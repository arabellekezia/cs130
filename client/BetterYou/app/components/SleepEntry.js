import React from "react";
import { StyleSheet, View } from "react-native";
import SummaryItem from "./SummaryItem";

import moment from "moment";

/**
 * This function produces a visual component that organizes and displays a single Sleep Entry in a visually appealing way
 * @param {StyleSheet} style Possible Additional stylesheet (optional)
 * @param {string} sleeptime timestamp string like "10:00 pm" that represents sleep start
 * @param {string} waketime timestamp string like "10:00 am" that represents time waking up
 * @param {number} minutes number of minutes slept
 * @returns {View} A View that contains everything to be displayed with the parameters filling in the details
 */
function SleepEntry({ style, sleeptime, waketime, minutes }) {
  const [sleeptimenum, sleeptimeunit] = parseTime(sleeptime);
  const [waketimenum, waketimeunit] = parseTime(waketime);

  return (
    <View style={{ ...styles.container, ...style }}>
      {/* TODO: This portion should be changed to accomodate calculations from backend data*/}
      <SummaryItem
        name="power-sleep"
        size={40}
        detail={sleeptimenum}
        unit={sleeptimeunit}
        label="Start time"
        iconColor="#A0BAFF"
        style={styles.summaryIndividual}
      />
      <SummaryItem
        name="alarm"
        size={40}
        detail={waketimenum}
        unit={waketimeunit}
        label="Arise time"
        iconColor="#A0BAFF"
        style={styles.summaryIndividual}
      />
      <SummaryItem
        name="sleep"
        size={40}
        detail={roundToOne(minutes / 60)}
        unit="Hours"
        label="Duration"
        iconColor="#A0BAFF"
        style={styles.summaryIndividual}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    //flex: 1,
    width: "100%",
    //marginTop: 25,
    //marginBottom: 25,
    // borderBottomWidth: 1,
    // borderTopWidth: 1,
    //borderRadius: 10,
    padding: 10,
  },
});

function parseTime(timestamp) {
  //takes in a timestamp string like "10:00 pm" and should parse it to 10:00 and "pm" for our summaryitem to use
  const timenum = moment(timestamp, "LT").format("hh:mm");
  const timeunit = moment(timestamp, "LT").format("A");

  return [timenum, timeunit];
}

function roundToOne(num) {
  return +(Math.round(num + "e+1") + "e-1");
}

export default SleepEntry;
