#ifndef _INTL_H_
#define _INTL_H_

typedef enum intl_strings_e
{
    LANGUAGE = 0,
    DATE_DM,
    TIME_HM,
    ELAPSED,
    MISSING1,
    MISSING2,
    MISSING3,
    STARTED,
    START,
    START_TODAY,
	MENU,
	ZAP,
	RECORD,
	CHANGE_GROUP,
	GO_TO_NOW,
	LG_24,
	PAGE_UD,
	MORE_INFO,
	CONFIGURATION,
	DATABASE_PATH,
	LOGS_PATH,
	SYNC_HOURS,
	SYNC_GROUPS,
	USB_PEN,
	TEMP_FOLDER,
	YES,
	NO,
	CUSTOM,
	HARD_DISK,
	START_SYNC,
	START_DOWNLOADER,
	SUNDAY,
	MONDAY,
	TUESDAY,
	WEDNESDAY,
	THURSDAY,
	FRIDAY,
	SATURADY,
	JANUARY,
	FEBRUARY,
	MARCH,
	APRIL,
	MAY,
	JUNE,
	JULY,
	AUGUST,
	SEPTEMBER,
	OCTOBER,
	NOVEMBER,
	DECEMBER,
	PROVIDERS,
	ERROR,
	SERIOUS_ERROR,
	CANNOT_OPEN_DGSDB,
	CANNOT_OPEN_LOG_FILE,
	NO_FAV_GROUPS,
	ERROR_OPEN_EPGDB,
	ERROR_READ_EPGDB,
	CANNOT_LOAD_PROVIDER,
	CANNOT_LOAD_DICTIONARY,
	SYNC_EPG,
	COMPLETED,
	READING_CHANNELS,
	READING_TITLES,
	PARSING_TITLES,
	READING_SUMMARIES,
	PARSING_SUMMARIES,
	SAVING_DATA,
	SKIN,
	STEP,
	TODAY,
	GRID,
	LIST,
	LIGHT,
	SCHEDULER,
	NO_TITLE,
	LINKED,
	SCHEDULER_ADD,
	SCHEDULER_DEL,
	LINKING_EVENTS
} intl_strings_t;

void intl_init ();
bool intl_read (char *file);
char *intl (intl_strings_t sid);

#endif // _INTL_H_
