import sys
from pathlib import Path
import quopri
import re
import base64
from icalendar import Calendar, vText
from datetime import datetime, timedelta, timezone
from typing import List, Optional

class Note:
    def __init__(self, type: str, last_modified: datetime, summary: Optional[str],
                description: Optional[str], photo: Optional[bytes], tz: str,
                decosuke: Optional[str], aalarm: Optional[str], status: Optional[str],
                due: Optional[str], location: Optional[str], show: Optional[str],
                original_vevent: Calendar):
        self.type = type
        self.last_modified = last_modified
        self.summary = summary
        self.description = description
        self.photo = photo
        self.tz = tz
        self.decosuke = decosuke
        self.aalarm = aalarm
        self.status = status
        self.due = due
        self.location = location
        self.show = show
        self.original_vevent = original_vevent

    def __repr__(self):
        return f"Note(type={self.type}, last_modified={self.last_modified}, summary={self.summary}, description={self.description}, photo={self.photo}, tz={self.tz}, decosuke={self.decosuke}, aalarm={self.aalarm}, status={self.status}, due={self.due}, location={self.location}, show={self.show})"
    
def _to_bytes(data) -> bytes:
    """データをバイト列に変換する"""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode('utf-8')
    if hasattr(data, 'to_ical'):
        return data.to_ical()
    if data is None:
        return b''
    raise TypeError(f"Unsupported type: {type(data)}")

def _to_str(data) -> Optional[str]:
    """データを文字列に変換する"""
    bdata = _to_bytes(data)
    if len(bdata) == 0:
        return None
    return bdata.decode('utf-8', errors='ignore')

def _clean_quoted_printable(data) -> bytes:
    """Quoted-Printableエンコーディングをデコードする"""
    return re.sub(rb';ENCODING=QUOTED-PRINTABLE:([\s\S]*?[^=])\r?\n', lambda x: b':' + re.sub(rb'\r?\n', b'\\\\n', quopri.decodestring(x[1])) + b"\r\n", data)

def _decode_image(image_b64) -> Optional[bytes]:
    """Base64エンコードされた画像データをデコードする"""
    if isinstance(image_b64, bytes):
        image_b64 = image_b64.decode('utf-8').strip()  # 空白や改行を削除
    if not image_b64:
        return None
    try:
        return base64.urlsafe_b64decode(image_b64 + '=' * (-len(image_b64) % 4))
    except base64.binascii.Error as e:
        print(f"Error decoding image: {e}", file=sys.stderr)
        return None

def _parse_datetime(datetime_str, tz_param=None) -> Optional[datetime]:
    """日付時刻文字列を解析し、datetimeオブジェクトを返す"""
    if tz_param:
        hours, minutes = map(int, tz_param.split(':'))
        tz = timezone(timedelta(hours=hours, minutes=minutes))
    else:
        tz = timezone.utc
    
    if hasattr(datetime_str, 'dt'):
        dt = datetime_str.dt.astimezone(tz)
    else:
        datetime_str = _to_str(datetime_str)
        if datetime_str is None or not datetime_str.strip():
            return None
        dt = datetime.strptime(datetime_str, '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc).astimezone(tz)
    return dt

def _parse_alarm(alarm_str, tz_param=None) -> Optional[datetime]:
    """アラーム文字列を解析し、datetimeオブジェクトを返す"""
    alarm_str = _to_str(alarm_str)
    if alarm_str is None or not alarm_str.strip():
        return None
    datetime_str = alarm_str.split(';')[0]
    if datetime_str.strip():
        return _parse_datetime(datetime_str.strip(), tz_param)
    return None

def parse_vcs_file(file_path) -> List[Note]:
    """VCSファイルを解析し、Noteオブジェクトのリストを返す"""
    ics_path = Path(file_path)
    data = ics_path.read_bytes()
    data = _clean_quoted_printable(data)

    try:
        calendar = Calendar.from_ical(data)
    except Exception as e:
        print("Error parsing iCal data:", e, file=sys.stderr)
        raise

    notes = []

    for event in calendar.walk('VEVENT'):
        type = event.get("X-DCM-TYPE", b'').upper()
        if isinstance(type, bytes):
            type = type.decode('utf-8')
        if type == "EVENT":
            continue

        # 修正: `SUMMARY`フィールドを文字列型にデコード
        summary = _to_str(event.get("SUMMARY"))
        description = _to_str(event.get("DESCRIPTION"))
        photo = _decode_image(event.get("X-DCM-PHOTO", vText(b"")).to_ical())
        tz = event.get("TZ", None)
        decosuke = _decode_image(event.get("X-DCM-DECOSUKE", vText(b"")))
        aalarm = _parse_alarm(event.get("AALARM", b""), tz)
        last_modified = _parse_datetime(event.get("LAST-MODIFIED", b""), tz)
        status = _to_str(event.get("STATUS"))
        due = _parse_datetime(event.get("DUE", b""), tz)
        location = _to_str(event.get("LOCATION"))
        show_str = _to_str(event.get("X-DCM-SHOW"))
        if show_str:
            show = show_str == "ON"
        else:
            show = None
        notes.append(Note(type, last_modified, summary, description, photo, tz, decosuke, aalarm, status, due, location, show, event))

    notes.sort(key=lambda e: e.last_modified)
    return notes