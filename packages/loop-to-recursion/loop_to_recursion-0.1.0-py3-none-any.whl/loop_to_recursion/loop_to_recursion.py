import ast
import contextlib
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path


def load_name(x: str) -> ast.Name:
    return ast.Name(id=x, ctx=ast.Load())


def store_name(x: str) -> ast.Name:
    return ast.Name(id=x, ctx=ast.Store())


def constant(x: bool | None) -> ast.Constant:
    return ast.Constant(value=x)


def load_tuple(xs: Iterable[str | bool | None | ast.expr]) -> ast.Tuple:
    expr = ast.Tuple(ctx=ast.Load())
    for x in xs:
        if isinstance(x, str):
            expr.elts.append(load_name(x))
        elif isinstance(x, bool | None):
            expr.elts.append(constant(x))
        else:
            expr.elts.append(x)
    return expr


def store_tuple(xs: Iterable[str | bool | None | ast.expr]) -> ast.Tuple:
    expr = ast.Tuple(ctx=ast.Store())
    for x in xs:
        if isinstance(x, str):
            expr.elts.append(store_name(x))
        elif isinstance(x, bool | None):
            expr.elts.append(constant(x))
        else:
            expr.elts.append(x)
    return expr


def get_names_from_arg(args: ast.arguments) -> list[str]:
    names: list[str] = []
    names.extend(arg.arg for arg in args.posonlyargs)
    names.extend(arg.arg for arg in args.args)
    names.extend(arg.arg for arg in args.kwonlyargs)
    if args.vararg:
        names.append(args.vararg.arg)
    if args.kwarg:
        names.append(args.kwarg.arg)
    return names


class LoopTransformer(ast.NodeTransformer):
    def __init__(self) -> None:
        self.stmts_prepend: list[list[ast.stmt]] = []
        self.stmts_append: list[list[ast.stmt]] = []
        self.counter: int = 0
        self.names_loaded: list[list[str]] = []
        self.names_stored: list[list[str]] = []
        self.names_nonlocal: list[list[str]] = []
        self.is_yielded: list[bool] = []
        self.is_awaited: list[bool] = []
        self.is_loop: list[bool] = []
        self.is_classdef: list[bool] = []
        self.stmt_break: list[ast.Return] = []
        self.stmt_continue: list[ast.Return] = []
        self.stmt_else: list[ast.Return] = []
        self.stmts_return: list[list[ast.Return]] = []

    def get_counter(self) -> int:
        self.counter += 1
        return self.counter

    @contextlib.contextmanager
    def context_stmt(self) -> Iterator[None]:
        self.stmts_prepend.append([])
        self.stmts_append.append([])
        yield
        prepends = self.stmts_prepend.pop()
        prepends_v = self.list_visit(prepends)
        prepends.clear()
        prepends.extend(prepends_v)
        appends = self.stmts_append.pop()
        appends_v = self.list_visit(appends)
        appends.clear()
        appends.extend(appends_v)

    @contextlib.contextmanager
    def context_scope(self, is_loop: bool = False, is_classdef: bool = False) -> Iterator[None]:
        self.names_loaded.append([])
        self.names_stored.append([])
        self.names_nonlocal.append([])
        self.is_yielded.append(False)
        self.is_awaited.append(False)
        self.is_loop.append(is_loop)
        if is_loop:
            self.stmt_break.append(ast.Return(value=constant(None)))
            self.stmt_continue.append(ast.Return(value=constant(None)))
            self.stmt_else.append(ast.Return(value=constant(None)))
            self.stmts_return.append([])
        self.is_classdef.append(is_classdef)
        yield
        self.names_loaded.pop()
        self.names_stored.pop()
        self.names_nonlocal.pop()
        self.is_yielded.pop()
        self.is_awaited.pop()
        if self.is_loop.pop():
            self.stmt_break.pop()
            self.stmt_continue.pop()
            self.stmt_else.pop()
            self.stmts_return.pop()
        self.is_classdef.pop()

    def list_visit(self, stmts: list[ast.stmt]) -> list[ast.stmt]:
        return [stmt_v for stmt in stmts for stmt_v in self.visit(stmt)]

    def stmt_visit(self, stmt: ast.stmt) -> list[ast.stmt]:
        with self.context_stmt():
            stmt_v = super().generic_visit(stmt)
            assert isinstance(stmt_v, ast.stmt)
            return [*self.stmts_prepend[-1], stmt_v, *self.stmts_append[-1]]

    def expr_visit(self, expr: ast.expr) -> ast.expr:
        expr_v = super().generic_visit(expr)
        assert isinstance(expr_v, ast.expr)
        return expr_v

    def generic_visit(self, node: ast.AST) -> ast.AST | list[ast.stmt]:  # type: ignore[override]
        if isinstance(node, ast.expr):
            return self.expr_visit(node)
        if isinstance(node, ast.stmt):
            return self.stmt_visit(node)
        return super().generic_visit(node)

    def visit_Global(self, stmt: ast.Global) -> list[ast.stmt]:
        self.names_nonlocal[-1].extend(stmt.names)
        return [stmt]

    def visit_Nonlocal(self, stmt: ast.Nonlocal) -> list[ast.stmt]:
        self.names_nonlocal[-1].extend(stmt.names)
        return [stmt]

    def visit_Name(self, expr: ast.Name) -> ast.Name:
        if isinstance(expr.ctx, ast.Store) and expr.id not in self.names_stored[-1]:
            self.names_stored[-1].append(expr.id)
        if isinstance(expr.ctx, ast.Load) and expr.id not in self.names_loaded[-1]:
            self.names_loaded[-1].append(expr.id)
        return expr

    def visit_Break(self, _: ast.Break) -> list[ast.stmt]:
        return [self.stmt_break[-1]]

    def visit_Continue(self, _: ast.Continue) -> list[ast.stmt]:
        return [self.stmt_continue[-1]]

    def visit_Return(self, stmt: ast.Return) -> list[ast.stmt]:
        stmt_v = self.stmt_visit(stmt)
        assert isinstance(stmt_v[-1], ast.Return)
        if self.is_loop[-1]:
            stmt_v[-1] = stmt_share = ast.Return(value=stmt_v[-1].value)
            self.stmts_return[-1].append(stmt_share)
        return stmt_v

    def get_names_from_target(self, expr: ast.AST) -> list[str]:
        if isinstance(expr, ast.Name):
            return [expr.id]
        if isinstance(expr, ast.Tuple):
            return [name for target in expr.elts for name in self.get_names_from_target(target)]
        return []

    def get_names_initialized(self, stmts: list[ast.stmt]) -> list[str]:
        if stmts == []:
            return []
        names: list[str] = []
        if isinstance(stmts[0], ast.Assign):
            for target in stmts[0].targets:
                names.extend(self.get_names_from_target(target))
            names.extend(self.get_names_initialized(stmts[1:]))
        elif isinstance(stmts[0], ast.FunctionDef | ast.AsyncFunctionDef):
            names.append(stmts[0].name)
        return names

    def skip_docstring(self, offset: int, stmts: list[ast.stmt]) -> int:
        if len(stmts) > offset:
            stmt = stmts[offset]
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                offset += 1
        return offset

    def skip_future_import(self, offset: int, stmts: list[ast.stmt]) -> int:
        if len(stmts) > offset:
            stmt = stmts[offset]
            if (
                isinstance(stmt, ast.ImportFrom)
                and stmt.module == "__future__"
                and isinstance(stmt.names[0], ast.alias)
                and stmt.names[0].name == "annotations"
            ):
                offset += 1
        return offset

    def prepend_initialize(self, offset: int, names_stored: set[str], stmts: list[ast.stmt]) -> None:
        if len(stmts) > offset:
            names = names_stored - set(self.get_names_initialized(stmts[offset:]))
            if len(names) > 0:
                if len(names) > 1:
                    prepend = ast.Assign(targets=[store_tuple(names)], value=load_tuple(None for _ in names))
                else:
                    prepend = ast.Assign(targets=[store_name(names.pop())], value=constant(None))
                stmts.insert(offset, prepend)

    def insert_initialize(self, names_stored: set[str], stmts: list[ast.stmt]) -> None:
        offset = self.skip_docstring(0, stmts)
        offset = self.skip_future_import(offset, stmts)
        self.prepend_initialize(offset, names_stored, stmts)

    def visit_ClassDef(self, stmt: ast.ClassDef) -> list[ast.stmt]:
        with self.context_scope(is_classdef=True):
            stmt_v = self.stmt_visit(stmt)
            assert isinstance(stmt_v[-1], ast.ClassDef)
            self.insert_initialize(set(self.names_stored[-1]), stmt_v[-1].body)
        return stmt_v

    def visit_Module(self, module: ast.Module) -> ast.Module:
        module_constants = {"__doc__"}
        with self.context_scope():
            module_v = self.generic_visit(module)
            assert isinstance(module_v, ast.Module)
            self.insert_initialize(set(self.names_stored[-1]) - module_constants, module_v.body)
        return module_v

    def process_functiondef(self, stmt: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.stmt]:
        with self.context_scope():
            names_arg = get_names_from_arg(stmt.args)
            self.names_stored[-1].extend(names_arg)
            stmt_v = self.stmt_visit(stmt)
            assert isinstance(stmt_v[-1], ast.FunctionDef | ast.AsyncFunctionDef)
            self.insert_initialize(set(self.names_stored[-1]) - set(self.names_nonlocal[-1]) - set(names_arg), stmt_v[-1].body)
        return stmt_v

    def visit_AsyncFunctionDef(self, stmt: ast.AsyncFunctionDef) -> list[ast.stmt]:
        return self.process_functiondef(stmt)

    def visit_FunctionDef(self, stmt: ast.FunctionDef) -> list[ast.stmt]:
        return self.process_functiondef(stmt)

    def process_comp(self, name: str, expr: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> ast.Call:
        name_iter = f"_iter_{self.get_counter()}"
        stmt: ast.stmt
        if isinstance(expr, ast.DictComp):
            stmt = ast.Expr(value=ast.Yield(value=load_tuple([expr.key, expr.value])))
        else:
            stmt = ast.Expr(value=ast.Yield(value=expr.elt))
        for comp in reversed(expr.generators):
            for i in reversed(comp.ifs):
                stmt = ast.If(test=i, body=[stmt])
            if comp.is_async:
                stmt = ast.AsyncFor(target=comp.target, iter=comp.iter, body=[stmt])
            else:
                stmt = ast.For(target=comp.target, iter=comp.iter, body=[stmt])
        assert isinstance(stmt, ast.For | ast.AsyncFor)
        stmt.iter = load_name(name_iter)
        stmt = ast.FunctionDef(name=name, args=ast.arguments([ast.arg(arg=name_iter)]), body=[stmt])
        self.stmts_prepend[-1].append(stmt)
        return ast.Call(func=load_name(name), args=[comp.iter])

    def visit_ListComp(self, expr: ast.ListComp) -> ast.Call:
        call = self.process_comp(f"_listcomp_{self.get_counter()}", expr)
        return ast.Call(func=load_name("list"), args=[call])

    def visit_SetComp(self, expr: ast.SetComp) -> ast.Call:
        call = self.process_comp(f"_setcomp_{self.get_counter()}", expr)
        return ast.Call(func=load_name("set"), args=[call])

    def visit_DictComp(self, expr: ast.DictComp) -> ast.Call:
        call = self.process_comp(f"_dictcomp_{self.get_counter()}", expr)
        return ast.Call(func=load_name("dict"), args=[call])

    def visit_GeneratorExp(self, expr: ast.GeneratorExp) -> ast.Call:
        return self.process_comp(f"_generatorexp_{self.get_counter()}", expr)

    def visit_Await(self, expr: ast.Await) -> ast.AST:
        self.is_awaited[-1] = True
        return self.expr_visit(expr)

    def visit_Yield(self, expr: ast.Yield) -> ast.AST:
        self.is_yielded[-1] = True
        return self.expr_visit(expr)

    def visit_YieldFrom(self, expr: ast.YieldFrom) -> ast.AST:
        self.is_yielded[-1] = True
        return self.expr_visit(expr)

    def get_names_arg(self) -> list[str]:
        names_classvar = []
        for names, is_classdef in zip(self.names_stored, self.is_classdef, strict=False):
            if is_classdef:
                names_classvar.extend(names)
        names_arg = [*self.names_stored[-1]]
        for name in self.names_loaded[-1]:
            if name in names_classvar and name not in names_arg:
                names_arg.append(name)
        return names_arg

    def get_call_next(self, name_func: str, names_arg: list[str]) -> ast.expr:
        args_call: list[ast.expr] = [load_name(name) for name in names_arg]
        call_next: ast.expr = ast.Call(func=load_name(name_func), args=args_call)
        if self.is_yielded[-1] and self.is_awaited[-1]:
            raise NotImplementedError("An asynchronous generator is not supported.")
        if self.is_yielded[-1]:
            call_next = ast.YieldFrom(value=call_next)
        if self.is_awaited[-1]:
            call_next = ast.Await(value=call_next)
        return call_next

    def update_stmt_break(self, exists_orelse: bool) -> None:
        names_break: list[str | bool | None | ast.expr] = [*self.names_stored[-1]]
        if len(self.stmts_return[-1]) > 0:
            names_break.extend([False, None])
        if exists_orelse:
            names_break.append(False)
        self.stmt_break[-1].value = load_tuple(names_break)

    def update_stmt_else(self, exists_orelse: bool) -> None:
        names_else: list[str | bool | None | ast.expr] = [*self.names_stored[-1]]
        if len(self.stmts_return[-1]) > 0:
            names_else.extend([False, None])
        if exists_orelse:
            names_else.append(True)
        self.stmt_else[-1].value = load_tuple(names_else)

    def update_stmt_continue(self, call_next: ast.expr) -> None:
        self.stmt_continue[-1].value = call_next

    def update_stmts_return(self, exists_orelse: bool) -> None:
        for stmt in self.stmts_return[-1]:
            names: list[str | bool | None | ast.expr] = [*self.names_stored[-1]]
            names.extend([True, stmt.value])
            if exists_orelse:
                names.append(False)
            stmt.value = load_tuple(names)

    def update_stmts_append(self, call_next: ast.expr, stmts_orelse: list[ast.stmt]) -> None:
        name_return_value = f"_return_value_{self.get_counter()}"
        name_return_flag = f"_return_flag_{self.get_counter()}"
        name_else_flag = f"_else_{self.get_counter()}"
        names_return: list[str | bool | None | ast.expr] = [*self.names_stored[-1]]
        if len(self.stmts_return[-1]) > 0:
            names_return.extend([name_return_flag, name_return_value])
        if len(stmts_orelse) > 0:
            names_return.append(name_else_flag)
        self.stmts_append[-1].append(ast.Assign(targets=[store_tuple(names_return)], value=call_next))
        if len(self.stmts_return[-1]) > 0:
            expr = load_name(name_return_flag)
            stmt = ast.Return(value=load_name(name_return_value))
            self.stmts_append[-1].append(ast.If(test=expr, body=[stmt]))
        if len(stmts_orelse) > 0:
            self.stmts_append[-1].append(ast.If(test=load_name(name_else_flag), body=stmts_orelse))

    def process_loop(self, name_func: str, stmts: list[ast.stmt], stmts_orelse: list[ast.stmt]) -> ast.stmt:
        names_arg = self.get_names_arg()
        call_next = self.get_call_next(name_func, names_arg)
        self.update_stmt_break(len(stmts_orelse) > 0)
        self.update_stmt_else(len(stmts_orelse) > 0)
        self.update_stmt_continue(call_next)
        self.update_stmts_return(len(stmts_orelse) > 0)
        self.update_stmts_append(call_next, stmts_orelse)
        args = ast.arguments([ast.arg(arg=name) for name in names_arg])
        return (ast.AsyncFunctionDef if self.is_awaited[-1] else ast.FunctionDef)(name_func, args, stmts)

    def visit_While(self, stmt: ast.While) -> list[ast.stmt]:
        name_func = f"_while_{self.get_counter()}"
        with self.context_stmt():
            self.names_stored[-1].append(name_func)
            orelse_v = self.list_visit(stmt.orelse)
            with self.context_scope(is_loop=True):
                self.names_loaded[-1].append(name_func)
                test_v = self.visit(stmt.test)
                body_v = self.list_visit(stmt.body)
                content_stmt = ast.If(test=test_v, body=[*body_v, self.stmt_continue[-1]], orelse=[self.stmt_else[-1]])
                func = self.process_loop(name_func, [content_stmt], orelse_v)
            return [*self.stmts_prepend[-1], func, *self.stmts_append[-1]]

    def process_for(self, stmt: ast.For | ast.AsyncFor) -> list[ast.stmt]:
        is_async = isinstance(stmt, ast.AsyncFor)
        name_func = f"_for_{self.get_counter()}"
        name_iter = f"_for_iter_{self.get_counter()}"
        with self.context_stmt():
            self.names_stored[-1].extend([name_func, name_iter])
            orelse_v = self.list_visit(stmt.orelse)
            with self.context_scope(is_loop=True):
                self.names_loaded[-1].extend([name_func, name_iter])
                next_id = "anext" if is_async else "next"
                next_call = ast.Call(func=load_name(next_id), args=[load_name(name_iter)])
                next_expr = ast.Await(value=next_call) if is_async else next_call
                next_stmt = ast.Assign(targets=[stmt.target], value=next_expr)
                next_stmt_v = self.stmt_visit(next_stmt)
                exc_id = "StopAsyncIteration" if is_async else "StopIteration"
                exc_handler = ast.ExceptHandler(load_name(exc_id), body=[self.stmt_else[-1]])
                body_v = self.list_visit(stmt.body)
                content_stmt = ast.Try(next_stmt_v, [exc_handler], [*body_v, self.stmt_continue[-1]])
                func = self.process_loop(name_func, [content_stmt], orelse_v)
            iter_id = "aiter" if is_async else "iter"
            iter_call = ast.Call(func=load_name(iter_id), args=[stmt.iter])
            iter_stmt = ast.Assign(targets=[store_name(name_iter)], value=iter_call)
            iter_stmt_v = self.stmt_visit(iter_stmt)
            self.stmts_prepend[-1].extend(iter_stmt_v)
            return [*self.stmts_prepend[-1], func, *self.stmts_append[-1]]

    def visit_AsyncFor(self, stmt: ast.AsyncFor) -> list[ast.stmt]:
        return self.process_for(stmt)

    def visit_For(self, stmt: ast.For) -> list[ast.stmt]:
        return self.process_for(stmt)


def loop_to_recursion(module: ast.Module) -> None:
    LoopTransformer().visit(module)
    ast.fix_missing_locations(module)


def cli() -> None:
    for name in sys.argv[1:]:
        with Path(name).open() as f:
            code = f.read()
        module = ast.parse(code, "<unknown>")
        loop_to_recursion(module)
        with Path(name).open("w") as f:
            print(ast.unparse(module), file=f)
