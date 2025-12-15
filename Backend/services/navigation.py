from flask import session
import logging

EXCLUDED_ENDPOINTS = {
    "static",
    "go_back",
    "auth.logout",
    "auth.login",
    "api_v1_bp",
    "api_v2_bp",
}

def push_nav(path):
    stack = session.get("nav_stack", [])
    #logging.warning(f"PUSH NAV: {path} | STACK BEFORE: {stack}")

    if not stack or stack[-1] != path:
        stack.append(path)

    session["nav_stack"] = stack
    #logging.warning(f"STACK AFTER: {stack}")



def pop_nav():
    stack = session.get("nav_stack", [])

    # Never pop the root ("/")
    if len(stack) > 1:
        stack.pop()

    session["nav_stack"] = stack
    return stack[-1] if stack else "/"
