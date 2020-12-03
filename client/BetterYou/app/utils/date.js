import moment from "moment";

const DateUtils = {
  // Given a moment, compute the dateFrom and dateTo to make a day query
  getDayTimeRange: (day) => {
    return {
      dateFrom: day.startOf("day").unix(),
      dateTo: day.endOf("day").add(1, "minute").unix(),
    };
  },
  // Get date objects for all the days in the current week
  // Can be used in weekly screens to pass date prop into each daily screen
  getDaysInWeek: () => {
    const weekStart = moment().startOf("week");
    const days = [];
    for (let i = 0; i <= 6; i++) {
      days.push(moment(weekStart).add(i, "days"));
      // console.log(DateUtils.getTodayTimeRange(days[i]))
    }
    return days;
  },
};

export default DateUtils;
