"""Interface Tkinter para o CRUD de registros."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from . import crud
from .errors import AppError, DatabaseError, ValidationError
from .models import Registro

COLUMNS: tuple[tuple[str, str, int], ...] = (
    # (chave, título, largura)
    ("id", "ID", 60),
    ("nome", "Nome", 220),
    ("email", "Email", 240),
    ("telefone", "Telefone", 140),
    ("criado_em", "Criado em", 150),
)


class CrudApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CRUD de Registros")
        self.geometry("940x580")
        self.minsize(780, 480)

        self._apply_theme()

        self._selected_id: int | None = None
        self._all_records: list[Registro] = []
        self._records_by_id: dict[int, Registro] = {}
        self._sort_key: str = "id"
        self._sort_desc: bool = True

        # ORDEM DE PACK: status bar ANTES da tabela para garantir reserva
        # de espaço na borda inferior (pack processa por ordem de chamada).
        self._build_form()
        self._build_buttons()
        self._build_search()
        self._build_status_bar()
        self._build_table()
        self._bind_shortcuts()

        self.entry_nome.focus_set()
        self.after(100, self.refresh)

    # -------------------- setup --------------------
    def _apply_theme(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Treeview", rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_form(self) -> None:
        frm = ttk.LabelFrame(self, text="Dados do registro")
        frm.pack(fill="x", padx=12, pady=(12, 6))

        self.var_nome = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telefone = tk.StringVar()

        ttk.Label(frm, text="Nome *").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.entry_nome = ttk.Entry(frm, textvariable=self.var_nome)
        self.entry_nome.grid(row=0, column=1, padx=6, pady=4, sticky="we")

        ttk.Label(frm, text="Email *").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.entry_email = ttk.Entry(frm, textvariable=self.var_email)
        self.entry_email.grid(row=0, column=3, padx=6, pady=4, sticky="we")

        ttk.Label(frm, text="Telefone").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.entry_telefone = ttk.Entry(frm, textvariable=self.var_telefone)
        self.entry_telefone.grid(row=1, column=1, padx=6, pady=4, sticky="we")

        for c in (1, 3):
            frm.columnconfigure(c, weight=1)

        for entry in (self.entry_nome, self.entry_email, self.entry_telefone):
            entry.bind("<Return>", self._on_enter_submit)

    def _build_buttons(self) -> None:
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=12, pady=6)

        ttk.Button(bar, text="Cadastrar", command=self.on_create).pack(side="left", padx=4)
        ttk.Button(bar, text="Atualizar", command=self.on_update).pack(side="left", padx=4)
        ttk.Button(bar, text="Excluir", command=self.on_delete).pack(side="left", padx=4)
        ttk.Button(bar, text="Limpar", command=self.clear_form).pack(side="left", padx=4)
        ttk.Button(bar, text="Recarregar (F5)", command=self.refresh).pack(side="right", padx=4)

    def _build_search(self) -> None:
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=12, pady=(0, 4))

        ttk.Label(bar, text="Buscar:").pack(side="left")
        self.var_search = tk.StringVar()
        self.var_search.trace_add("write", lambda *_: self._apply_filter())
        entry = ttk.Entry(bar, textvariable=self.var_search, width=40)
        entry.pack(side="left", padx=6)
        ttk.Button(bar, text="Limpar busca", command=lambda: self.var_search.set("")).pack(
            side="left"
        )

    def _build_status_bar(self) -> None:
        self.var_status = tk.StringVar(value="Pronto.")
        status = ttk.Label(self, textvariable=self.var_status, anchor="w", relief="sunken")
        status.pack(fill="x", side="bottom")

    def _build_table(self) -> None:
        wrapper = ttk.Frame(self)
        wrapper.pack(fill="both", expand=True, padx=12, pady=(4, 6))

        keys = tuple(k for k, _, _ in COLUMNS)
        self.tree = ttk.Treeview(wrapper, columns=keys, show="headings", selectmode="browse")

        for key, title, width in COLUMNS:
            self.tree.heading(key, text=title, command=lambda k=key: self._on_sort(k))
            anchor = "center" if key == "id" else "w"
            self.tree.column(key, width=width, anchor=anchor, stretch=True)

        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(wrapper, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="we")
        wrapper.rowconfigure(0, weight=1)
        wrapper.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _bind_shortcuts(self) -> None:
        self.bind("<F5>", lambda _e: self.refresh())
        self.bind("<Escape>", lambda _e: self.clear_form())
        self.bind("<Control-n>", lambda _e: (self.clear_form(), self.entry_nome.focus_set()))
        self.bind("<Delete>", self._on_shortcut_delete)

    def _on_shortcut_delete(self, _event: tk.Event) -> None:
        # Não dispara se o usuário estiver editando um Entry.
        focus = self.focus_get()
        if isinstance(focus, (ttk.Entry, tk.Entry)):
            return
        self.on_delete()

    def _on_enter_submit(self, _event: tk.Event) -> str:
        # Enter no formulário: atualiza se houver seleção, senão cadastra.
        if self._selected_id is not None:
            self.on_update()
        else:
            self.on_create()
        return "break"

    # -------------------- helpers --------------------
    def _collect(self) -> tuple[str, str, str]:
        return (
            self.var_nome.get().strip(),
            self.var_email.get().strip(),
            self.var_telefone.get().strip(),
        )

    def _handle_error(self, exc: AppError) -> None:
        if isinstance(exc, ValidationError):
            messagebox.showwarning("Validação", str(exc), parent=self)
        elif isinstance(exc, DatabaseError):
            messagebox.showerror("Erro no banco", str(exc), parent=self)
        else:
            messagebox.showerror("Erro", str(exc), parent=self)

    def _set_status(self, msg: str) -> None:
        # Defensivo: status bar pode não existir se chamado antes do build.
        var = getattr(self, "var_status", None)
        if var is not None:
            var.set(msg)

    # -------------------- actions --------------------
    def on_create(self) -> None:
        nome, email, telefone = self._collect()
        try:
            new_id = crud.create_registro(nome, email, telefone)
        except AppError as exc:
            self._handle_error(exc)
            return
        self._set_status(f"Registro #{new_id} cadastrado.")
        self.clear_form()
        self.refresh()

    def on_update(self) -> None:
        if self._selected_id is None:
            messagebox.showwarning("Atenção", "Selecione um registro na tabela.", parent=self)
            return
        nome, email, telefone = self._collect()
        try:
            crud.update_registro(self._selected_id, nome, email, telefone)
        except AppError as exc:
            self._handle_error(exc)
            return
        self._set_status(f"Registro #{self._selected_id} atualizado.")
        self.refresh()

    def on_delete(self) -> None:
        if self._selected_id is None:
            messagebox.showwarning("Atenção", "Selecione um registro na tabela.", parent=self)
            return
        if not messagebox.askyesno(
            "Confirmação", f"Excluir o registro #{self._selected_id}?", parent=self
        ):
            return
        deleted_id = self._selected_id
        try:
            crud.delete_registro(deleted_id)
        except AppError as exc:
            self._handle_error(exc)
            return
        self._set_status(f"Registro #{deleted_id} excluído.")
        self.clear_form()
        self.refresh()

    def clear_form(self) -> None:
        self._selected_id = None
        self.var_nome.set("")
        self.var_email.set("")
        self.var_telefone.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.entry_nome.focus_set()

    def refresh(self) -> None:
        keep_id = self._selected_id
        try:
            self._all_records = crud.list_registros()
        except AppError as exc:
            self._selected_id = None
            self._all_records = []
            self._records_by_id = {}
            self._handle_error(exc)
            self._set_status("Falha ao carregar registros.")
            return
        self._records_by_id = {r.id: r for r in self._all_records}
        self._render_rows(keep_id)
        self._set_status(f"{len(self._all_records)} registro(s) carregado(s).")

    # -------------------- rendering --------------------
    def _apply_filter(self) -> None:
        self._render_rows(self._selected_id)
        total = len(self._all_records)
        shown = len(self.tree.get_children())
        if self.var_search.get().strip():
            self._set_status(f"Exibindo {shown} de {total} registro(s) (filtro aplicado).")
        else:
            self._set_status(f"{total} registro(s) carregado(s).")

    def _filtered_records(self) -> list[Registro]:
        term = self.var_search.get().strip().lower()
        if not term:
            records = list(self._all_records)
        else:
            records = [
                r for r in self._all_records
                if term in r.nome.lower()
                or term in r.email.lower()
                or term in (r.telefone or "").lower()
            ]
        return self._sorted(records)

    def _sorted(self, records: list[Registro]) -> list[Registro]:
        key = self._sort_key

        def _value(r: Registro):
            v = getattr(r, key, None)
            if v is None:
                return ""
            if isinstance(v, str):
                return v.lower()
            return v

        return sorted(records, key=_value, reverse=self._sort_desc)

    def _render_rows(self, keep_id: int | None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        found = False
        for r in self._filtered_records():
            criado = r.criado_em.strftime("%d/%m/%Y %H:%M") if r.criado_em else ""
            self.tree.insert(
                "",
                "end",
                iid=str(r.id),
                values=(r.id, r.nome, r.email, r.telefone or "", criado),
            )
            if keep_id is not None and r.id == keep_id:
                found = True

        if keep_id is not None and found:
            self.tree.selection_set(str(keep_id))
            self.tree.see(str(keep_id))
        else:
            self._selected_id = None

        self._update_sort_indicators()

    def _update_sort_indicators(self) -> None:
        arrow = " ▼" if self._sort_desc else " ▲"
        for key, title, _ in COLUMNS:
            text = title + arrow if key == self._sort_key else title
            self.tree.heading(key, text=text)

    def _on_sort(self, key: str) -> None:
        if key == self._sort_key:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_key = key
            self._sort_desc = False
        self._render_rows(self._selected_id)

    def _on_select(self, _event: tk.Event) -> None:
        sel = self.tree.selection()
        if not sel:
            self._selected_id = None
            return
        try:
            rid = int(sel[0])
        except ValueError:
            self._selected_id = None
            return
        # Busca o registro no cache (preserva tipos: leading zeros, None, etc).
        registro = self._records_by_id.get(rid)
        if registro is None:
            self._selected_id = None
            return
        self._selected_id = rid
        self.var_nome.set(registro.nome)
        self.var_email.set(registro.email)
        self.var_telefone.set(registro.telefone or "")
