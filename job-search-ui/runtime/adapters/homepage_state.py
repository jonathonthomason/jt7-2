from typing import Any, Callable, Dict


def build_homepage_state(selectors: Any) -> Dict[str, Any]:
    return {
        'summary': selectors.getTodayPlanSummary(),
        'next_best_action': selectors.getNextBestAction(),
        'execution_cards': selectors.getExecutionCards(),
        'completed_today': selectors.getCompletedToday(),
        'waiting_actions': selectors.getWaitingActions(),
        'recent_signals': selectors.getRecentSignals(),
        'latest_task_run': selectors.getLatestTaskRun(),
    }


def homepage_sections_available() -> Dict[str, bool]:
    return {
        'next_best_action': True,
        'supporting_actions': True,
        'recent_signals': True,
        'completed_today': True,
        'waiting': True,
        'run_status': True,
    }
