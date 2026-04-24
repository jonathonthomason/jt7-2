from runtime.adapters.homepage_state import build_homepage_state


def build_todays_plan_state(selectors_module):
    return build_homepage_state(selectors_module)
