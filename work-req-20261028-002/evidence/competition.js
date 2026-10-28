(function (gsa) {
    gsa.libs = gsa.libs || {}
    gsa.init = gsa.init || {}

    const SELECTORS = {
        COMPETITION_WIDGET: '.gsa-competition-widget',
        CALENDAR: '.gsa-comp-calendar',
        BOX_COLLAPSE: '.gsa-comp-box-collapse',
        LOADER: '.gsa-loader'
    };

    const ENDPOINTS = {
        SPORT_COMPETITION: 'widget/sport_competition',
        MATCH_COMPETITION_ROUND: 'widget/match_competition_round',
        MATCH_COMPETITION_ROUND_GAMEWEEK: 'widget/match_competition_round_gameweek'
    };

    const getWidgetData = ($widget) => ({
        sport: $widget.data('sport'),
        roundId: $widget.data('round_id'),
        competitionId: $widget.data('competition_id'),
        roundKey: $widget.data('round_key'),
        current: $widget.data('current'),
        weeks: $widget.data('weeks'),
        clearOnCollapse: $widget.data('clear_on_collapse'),
    });

    const showLoader = ($container) => {
        $container.html('<div class="gsa-flex-center"><div class="gsa-loader gsa-my-8"></div></div>');
    };

    const removeLoader = () => {
        $(SELECTORS.LOADER).remove();
    };

    const handleError = (error, $container) => {
        console.error('Error loading competition data:', error);
        $container.html('<div class="gsa-error-message">Failed to load competition data. Please try again later.</div>');
    };

    const initializeComponents = ($calendar, type, roundId) => {
        if (!roundId) {
            gsa.libs.loadDropdownSelector({ prefix: SELECTORS.COMPETITION_WIDGET, type }, loadData);
        } else {
            gsa.libs.loadCalendar({
                calendar: $calendar,
                type
            }, loadData);
        }
        gsa.libs.loadCollapseTableItem();
        gsa.libs.loadExpandTable();
        gsa.libs.loadSimplebar();
        gsa.libs.loadBoxCollapse({});
    };

    const loadData = async function ($widget, selectedValue, type) {
        const $container = $(SELECTORS.COMPETITION_WIDGET);
        try {
            const widgetData = getWidgetData($widget);
            const currentLang = gsa.libs.getCurrentLanguage();
            showLoader($container);
            const baseUrl = type === 'widget'
                ? gsa.libs.getRequestUrl(`${currentLang}/${ENDPOINTS.SPORT_COMPETITION}`)
                : `/${currentLang}/${ENDPOINTS.SPORT_COMPETITION}`;
            const requestData = {
                sport: widgetData.sport,
                current: selectedValue,
                roundKey: widgetData.roundId ? `${widgetData.roundId}_${selectedValue}` : selectedValue,
                type: widgetData.roundId ? 'match' : 'round',
                competitionId: widgetData.competitionId
            };
            const response = await $.ajax({
                url: baseUrl,
                type: 'POST',
                data: requestData,
                timeout: 10000
            });
            removeLoader();
            $container.html(response);
            initializeComponents($widget, type, widgetData.roundId);
        } catch (error) {
            handleError(error, $container);
        }
    };

    const loadMatchCompetitionData = async function ($widget, type, roundType, data) {
        const $container = $widget.siblings().eq(0);

        try {
            const widgetData = getWidgetData($widget);

            if (widgetData.clearOnCollapse === false) {
                return;
            }

            const currentLang = type == 'widget' ? $widget.closest('.gsa-widget').data('lang') : gsa.libs.getCurrentLanguage();
            let activeSubRoundKey;    		  
			const currentRound = widgetData.current;
			const roundKey = widgetData.roundKey ? widgetData.roundKey : (currentRound ? currentRound.split('_')[0] : null);

			if (roundType === 'gameweek' || roundType === 'page') {
				const activeWeek = data.activeWeek;
				activeSubRoundKey = widgetData.weeks ? Object.keys(widgetData.weeks)[activeWeek] : null;
			} else if (roundType === 'date') {
				activeSubRoundKey = roundKey + '_' + data.current;
			}
			const url = type === 'widget'
				? gsa.libs.getRequestUrl(`${currentLang}/${ENDPOINTS.MATCH_COMPETITION_ROUND_GAMEWEEK}`)
				: `/${currentLang}/${ENDPOINTS.MATCH_COMPETITION_ROUND_GAMEWEEK}`;
           
            showLoader($container);

            const response = await $.ajax({
                url: url,
                type: 'POST',
                data: {
                    sport: widgetData.sport,
                    roundKey,
                    activeSubRoundKey,
                    wid: $widget.closest('.gsa-widget[data-wid]').data('wid') ?? '',
                    client_brand: $widget.closest('.gsa-widget[data-wid]').data('brand') ?? '',
                    client_brand_version: $widget.closest('.gsa-widget[data-wid]').data('version') ?? '',
                    user_timezone: Intl?.DateTimeFormat?.()?.resolvedOptions?.()?.timeZone || 'Europe/Berlin',
                    isActiveRound: data.isActiveRound ?? '',
                    competitionId: widgetData.competitionId
                },
                timeout: 10000
            });

            removeLoader();
            $container.html(response);

            if (roundType !== 'gameweek' && roundType !== 'date' && roundType !== 'page' && $(SELECTORS.CALENDAR).length > 0) {
                gsa.libs.loadCalendar({
                    calendar: $widget.siblings().find('.gsa-comp-calendar'),
                    type,
                    page: 'page'
                }, loadMatchCompetitionData);
            }
			
            gsa.libs.loadExpandTable();
            gsa.libs.loadSimplebar();
        } catch (error) {        
            handleError(error, $container);
        }
    };

    gsa.init.initCompetitionWidget = function (type = 'widget') {
        try {
            gsa.libs.loadDropdownSelector({ prefix: '', type }, loadData);
            if ($(SELECTORS.CALENDAR).length > 0) {
                $(SELECTORS.CALENDAR).each(function () {
                    const $calendar = $(this);
                    gsa.libs.loadCalendar({
                        calendar: $calendar,
                        type
                    }, loadData);
                });
            }
            gsa.libs.loadCollapseTableItem();
            if (type === 'widget') {
                gsa.libs.loadExpandTable();
                gsa.libs.loadSimplebar();
                gsa.libs.loadBoxCollapse({});
            }
        } catch (error) {
            console.error('Error initializing competition widget:', error);
        }
    };

    gsa.init.initMatchCompetitionWidget = function (type = 'widget') {
        try {
            if ($(SELECTORS.CALENDAR).length > 0) {
                $(SELECTORS.CALENDAR).each(function () {
                    const $calendar = $(this);
                    gsa.libs.loadCalendar({
                        calendar: $calendar,
                        type,
                        page: 'competition'
                    }, loadMatchCompetitionData);
                });
            }
            if ($(SELECTORS.BOX_COLLAPSE).length > 0) {
                gsa.libs.loadBoxCollapse({ type }, loadMatchCompetitionData);
            }
            if (type === 'widget') {
                gsa.libs.loadExpandTable();
                gsa.libs.loadSimplebar();
            }
        } catch (error) {
            console.error('Error initializing match competition widget:', error);
        }
    };

    const cleanup = () => {
        $(SELECTORS.COMPETITION_WIDGET).off();
        $(SELECTORS.CALENDAR).off();
        $(SELECTORS.BOX_COLLAPSE).off();
    };

    window.addEventListener('beforeunload', cleanup);

})(window.gsa = window.gsa || {});
