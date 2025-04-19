import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Tuple, Union


class JUnitReporter:
    def __init__(self, output_path: str = "junit.xml") -> None:
        self.output_path = output_path

    @staticmethod
    def _normalize(val: Any) -> str:
        return str(val).replace("\n", " ")

    @staticmethod
    def _format_table(headers: Tuple[str, str], rows: List[Tuple[str, str]]) -> str:
        if not rows:
            return ""

        col_widths = [max(len(h), max(len(str(row[i])) for row in rows)) for i, h in enumerate(headers)]

        def format_row(row: Tuple[str, str]) -> str:
            return "│ " + " │ ".join(f"{str(col): <{w}}" for col, w in zip(row, col_widths)) + " │"

        line = "├" + "┬".join("─" * (w + 2) for w in col_widths) + "┤"
        top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
        bottom = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"

        table = [top, format_row(headers), line]
        for row in rows:
            table.append(format_row(row))
        table.append(bottom)
        return "\n".join(table)

    def _format_reason(self, reason_dict: Dict[str, Any], service_item: str) -> str:
        try:
            rows: List[Tuple[str, str]] = []
            for field, reason in reason_dict.items():
                if isinstance(reason, list):
                    for item in reason:
                        rows.append((field, self._normalize(item)))
                elif isinstance(reason, dict):
                    for subfield, subreason in reason.items():
                        rows.append((f"{field}.{subfield}", self._normalize(subreason)))
                else:
                    rows.append((field, self._normalize(reason)))

            title = service_item or "-"
            table = self._format_table(("Field", "Reason"), rows)
            return f"\n{title}\n{table}\n"
        except Exception as e:
            return f"Error formatting reason for {service_item}: {str(e)}"

    def write(self, errors: Dict[str, Dict[str, Dict[str, Any]]]) -> None:
        testsuite = ET.Element("testsuite", name="NetOrca Validation")
        failure_count = 0

        for repo, apps in errors.items():
            for app_name, services in apps.items():
                if not isinstance(services, dict):
                    continue
                for service_name, service_items in services.items():
                    if not isinstance(service_items, dict):
                        continue

                    classname = app_name
                    test_name = f"{app_name} - {service_name}"

                    if service_name == "metadata":
                        error_count = sum(len(v) if isinstance(v, (list, dict)) else 1 for v in service_items.values())
                        if error_count == 0:
                            continue

                        failure_count += 1
                        testcase = ET.SubElement(testsuite, "testcase", classname=classname, name=test_name)
                        failure = ET.SubElement(testcase, "failure")
                        failure.text = self._format_reason(service_items, "metadata")

                    else:
                        grouped: Dict[str, Dict[str, Any]] = {
                            service_item: fields
                            for service_item, fields in service_items.items()
                            if isinstance(fields, dict)
                        }

                        if not grouped:
                            continue

                        error_count = sum(
                            len(v) if isinstance(v, (list, dict)) else 1
                            for fields in grouped.values()
                            for v in fields.values()
                        )
                        if error_count == 0:
                            continue

                        failure_count += 1
                        testcase = ET.SubElement(testsuite, "testcase", classname=classname, name=test_name)
                        failure = ET.SubElement(testcase, "failure")
                        failure.text = "\n".join(
                            self._format_reason(fields, service_item) for service_item, fields in grouped.items()
                        )

        testsuite.set("tests", str(failure_count))
        testsuite.set("failures", str(failure_count))
        try:
            ET.ElementTree(testsuite).write(self.output_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(f"Failed to write JUnit XML: {e}")
