from filesystem_monitor import monitor_filesystem
from LOG_TO_SPLUNK import log_attack
from db import create_database, log_filesystem_change
from Report import generate_daily_report

def flatten_dict(d, parent_key='', sep='_'):
    """Flatten một dictionary lồng nhau."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    """Hàm chính điều khiển chương trình."""
    create_database()

    for change in monitor_filesystem():
        log_filesystem_change(change['action'], change['details'])

        flattened_change = flatten_dict(change)
        log_attack(event_type="filesystem_change", **flattened_change)

    generate_daily_report() 

if __name__ == "__main__":
    main()