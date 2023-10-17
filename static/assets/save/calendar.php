<?php
// Datos del evento
$titulo = "XV Ivonne";
$fecha_inicio = "2023-11-11 14:30:00";
$fecha_fin = "2023-11-11 22:30:00";
$zona_horaria = "America/Mexico_City";

// Crea el contenido del archivo .ics
$contenido_ics = "BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//OpenACME Corp.//Event Calendar//EN
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:{$zona_horaria}
LAST-MODIFIED:20201011T015911Z
X-LIC-LOCATION:{$zona_horaria}
BEGIN:DAYLIGHT
TZNAME:CDT
TZOFFSETFROM:-0600
TZOFFSETTO:-0500
DTSTART:19700405T020000
RRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU
END:DAYLIGHT
BEGIN:STANDARD
TZNAME:CST
TZOFFSETFROM:-0500
TZOFFSETTO:-0600
DTSTART:19701025T020000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
DTSTAMP:" . gmdate('Ymd\THis\Z') . "
UID:1260@invitacionesparaeventos.com
DTSTART;TZID={$zona_horaria}:" . date('Ymd\THis', strtotime($fecha_inicio)) . "
DTEND;TZID={$zona_horaria}:" . date('Ymd\THis', strtotime($fecha_fin)) . "
SUMMARY:{$titulo}
URL:
DESCRIPTION:
LOCATION:
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:
TRIGGER:-PT24H
END:VALARM
END:VEVENT
END:VCALENDAR";

// Configura las cabeceras del archivo .ics
header('Content-type: text/calendar; charset=utf-8');
header('Content-Disposition: attachment; filename=XVIvonne.ics');

// Envía el contenido del archivo .ics al navegador
echo $contenido_ics;
?>
