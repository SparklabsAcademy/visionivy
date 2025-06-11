"""Simple Reflex app with admin login and management page."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """Application state handling login and consultant management."""

    username: str = ""
    password: str = ""
    login_error: str = ""
    new_consultant: str = ""
    consultants: list[str] = []

    def login(self) -> rx.event.EventSpec:
        """Validate credentials and redirect if admin."""
        if self.username == "admin" and self.password == "admin":
            return rx.redirect("/admin")
        self.login_error = "Invalid credentials"

    def add_consultant(self) -> None:
        """Add a consultant to the list."""
        if self.new_consultant:
            self.consultants.append(self.new_consultant)
            self.new_consultant = ""


def login_page() -> rx.Component:
    """Login page displayed at the index route."""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading("Login", size="6"),
                rx.input(
                    placeholder="Username",
                    on_change=State.set_username,
                    value=State.username,
                ),
                rx.input(
                    placeholder="Password",
                    type_="password",
                    on_change=State.set_password,
                    value=State.password,
                ),
                rx.button("Sign In", on_click=State.login),
                rx.cond(State.login_error != "", rx.text(State.login_error, color="red")),
                spacing="4",
            ),
            padding="8",
            border_radius="8",
            box_shadow="md",
        ),
        height="100vh",
    )


def admin_page() -> rx.Component:
    """Page to manage consultant accounts after admin login."""
    return rx.container(
        rx.heading("Consultant Management", size="7"),
        rx.hstack(
            rx.input(
                placeholder="New consultant name",
                on_change=State.set_new_consultant,
                value=State.new_consultant,
            ),
            rx.button("Add", on_click=State.add_consultant),
        ),
        rx.vstack(
            rx.foreach(
                State.consultants,
                lambda name: rx.text(name, padding_y="1"),
            ),
            align_items="start",
        ),
        spacing="6",
        padding_top="4",
    )


app = rx.App()
app.add_page(login_page, route="/")
app.add_page(admin_page, route="/admin")

