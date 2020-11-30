import React from 'react';
import { StyleSheet, View } from 'react-native';
import SummaryItem from './SummaryItem';

import moment from "moment";

function SleepEntry({
  style,
  sleeptime,
  waketime,
}) {
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
        label="Started Sleep"
        style={styles.summaryindividual}
      />
      <SummaryItem
        name="alarm"
        size={40}
        detail={waketimenum}
        unit={waketimeunit}
        label="Woke Up"
        style={styles.summaryindividual}
      />
      <SummaryItem
        name="sleep"
        size={40}
        detail={5.6}
        unit="Hours"
        label="Time Slept"
        style={styles.summaryindividual}
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
    borderWidth: 0.5,
    //borderRadius: 10,
    padding: 10,
  },
})

function parseTime(timestamp) {
  //takes in a timestamp string like "10:00 pm" and should parse it to 10:00 and "pm" for our summaryitem to use
  const timenum = moment(timestamp, "LT").format("hh:mm");
  const timeunit = moment(timestamp, "LT").format("A");
  
  return [timenum, timeunit];
}

export default SleepEntry;