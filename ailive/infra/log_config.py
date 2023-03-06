import sys
import logbook

logger = logbook.Logger('AI Live Logger')
logbook.StreamHandler(sys.stdout).push_application()
logbook.TimedRotatingFileHandler('ai_live.log', backup_count=5).push_application()

