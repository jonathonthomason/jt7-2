#!/usr/bin/env python3
import json
import sys

try:
    from jobspy import scrape_jobs
except Exception as e:
    print(json.dumps({
        "ok": False,
        "error": f"failed_to_import_jobspy: {e}"
    }))
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "ok": False,
            "error": "missing_query",
            "usage": "jobspy_wrapper.py '<json-args>'"
        }))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": f"invalid_json_args: {e}"
        }))
        sys.exit(1)

    site_names = args.get("site_names", ["indeed", "linkedin", "google"])
    search_term = args.get("search_term", "Product Designer")
    location = args.get("location", "Remote")
    results_wanted = int(args.get("results_wanted", 20))
    hours_old = int(args.get("hours_old", 168))
    country_indeed = args.get("country_indeed", "USA")

    try:
        jobs = scrape_jobs(
            site_name=site_names,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed,
        )
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": f"scrape_failed: {e}"
        }))
        sys.exit(1)

    try:
        records = jobs.to_dict(orient="records")
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": f"to_dict_failed: {e}"
        }))
        sys.exit(1)

    print(json.dumps({
        "ok": True,
        "count": len(records),
        "jobs": records
    }, default=str))

if __name__ == "__main__":
    main()
