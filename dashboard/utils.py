from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font


def export_bookings_excel(bookings):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bookings"

    headers = [
        "Reference",
        "Customer",
        "Email",
        "Phone",
        "Service",
        "Status",
        "Preferred Date",
        "Preferred Time",
        "Address",
        "Device Info",
        "Notes",
        "Created At",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for booking in bookings:
        ws.append([
            booking.reference,
            booking.customer.name,
            booking.customer.email,
            booking.customer.phone,
            booking.service.name,
            booking.get_status_display(),
            booking.preferred_date.isoformat(),
            booking.preferred_time.strftime("%H:%M"),
            booking.service_address,
            booking.device_info,
            booking.notes,
            booking.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    for column in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = min(max_length + 2, 50)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="techcare_bookings.xlsx"'
    return response
