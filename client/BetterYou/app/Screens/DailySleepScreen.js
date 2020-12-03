import React, { useEffect, useState } from "react";
import { SafeAreaView, ScrollView, StyleSheet, View } from "react-native";

import { groupBy } from "lodash";

import AppText from "../components/AppText";
import TitleText from "../components/TitleText";

import moment from "moment";
import TextButton from "../components/TextButton";
import DailySleepEntries from "../components/DailySleepEntries";
import SleepService from "../services/SleepService";

function DailySleepScreen({ route }) {
  const [isReady, setReady] = useState(false);
  const [sleepEntries, setSleepEntries] = useState({ sleep: [], naps: [] });

  const date = route.params ? route.params.date : Date.now();

  useEffect(() => {
    loadSleepEntries();
  }, []);

  const loadSleepEntries = async () => {
    setReady(false);
    const entries = await getTodaySleepEntries(date);
    setSleepEntries(entries);
    setReady(true);
  };

  return (
    <SafeAreaView>
      {isReady && (
        <ScrollView
          alwaysBounceVertical={false}
          contentContainerStyle={styles.container}
        >
          <TitleText style={styles.pageTitle} children="Sleep" />
          <AppText style={styles.dateHeader} children={getToday(date)} />
          {/*<View style={styles.sleepsummary}>
            {/* TODO: This portion should be changed to accomodate calculations from backend data 
            <SummaryItem
              name="power-sleep"
              size={40}
              detail="1:30"
              unit="AM"
              label="Started Sleep"
              style={styles.summaryindividual}
            />
            <SummaryItem
              name="alarm"
              size={40}
              detail="7:10"
              unit="AM"
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
          */}

          <DailySleepEntries
            style={styles.sleepLog}
            headerTextStyle={styles.sleepEntryHeader}
            headerText="Last night"
            entries={sleepEntries.sleep}
          />

          <DailySleepEntries
            style={styles.sleepLog}
            headerTextStyle={styles.sleepEntryHeader}
            headerText="Recorded naps"
            entries={sleepEntries.naps}
          />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
    marginBottom: 24,
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 8,
  },
  sleepLog: {
    marginTop: 12,
  },
  sleepEntryHeader: {
    marginLeft: "5%",
  },
  sleepsummary: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    //flex: 1,
    width: "100%",
    marginTop: 25,
    //marginBottom: 25,
    borderWidth: 1,
    //borderRadius: 10,
    padding: 10,
  },
  summaryindividual: {
    //borderWidth: 1,
    //borderRadius: 10,
    marginHorizontal: 5,
    //backgroundColor: "#d5f7f7",
  },
});

/**
 *
 * @param {Number} date: the number of milliseconds since the Unix Epoch (Jan 1 1970 12AM UTC).
 */
function getToday(date) {
  //making this function in case this has to work with backend if not might simplify later
  return moment(date).format("dddd, MMMM Do");
}

/**
 *
 * @param {Number} date: the number of milliseconds since the Unix Epoch (Jan 1 1970 12AM UTC).
 */

async function getTodaySleepEntries(date) {
  //TODO: change from hardcoded to integration
  /* Note from evan - backend allows us to differentiate between naps + actual sleep, so i'm using that info */

  // return {
  //   sleep: {
  //     sleeptime: "10:00 pm",
  //     waketime: "6:00 am",
  //   },
  //   naps: [
  //     {
  //       sleeptime: "11:00 pm",
  //       waketime: "8:00 am",
  //     },
  //     {
  //       sleeptime: "11:00 pm",
  //       waketime: "8:00 am",
  //     },
  //   ],
  // };
  try {
    const sleepEntries = await SleepService.getDailySleepEntries(date);
    const groupedSleepEntries = await groupSleepByCategory(sleepEntries);
    return groupedSleepEntries;
  } catch (err) {
    console.log(err);
  }
}

async function groupSleepByCategory(sleepEntries) {
  try {
    const groupedEntries = groupBy(sleepEntries, "Nap");

    let naps = [];
    let sleep = [];
    if (groupedEntries.hasOwnProperty("0")) {
      for (let i = 0; i < groupedEntries["0"].length; i++) {
        const sleepTimeSeconds = groupedEntries["0"][i].SleepTime;
        const wakeTimeSeconds = groupedEntries["0"][i].WakeupTime;

        sleep.push({
          sleeptime: moment(sleepTimeSeconds * 1000).format("LT"),
          waketime: moment(wakeTimeSeconds * 1000).format("LT"),
          minutes: groupedEntries["0"][i].Minutes,
        });
      }
    }

    if (groupedEntries.hasOwnProperty("1")) {
      for (let i = 0; i < groupedEntries["1"].length; i++) {
        const sleepTimeSeconds = groupedEntries["1"][i].SleepTime;
        const wakeTimeSeconds = groupedEntries["1"][i].WakeupTime;

        naps.push({
          sleeptime: moment(sleepTimeSeconds * 1000).format("LT"),
          waketime: moment(wakeTimeSeconds * 1000).format("LT"),
          minutes: groupedEntries["1"][i].Minutes,
        });
      }
    }
    let res = {
      sleep: sleep,
      naps: naps,
    };

    console.log(res);
    return res;
  } catch (err) {
    throw new Error(err);
  }
}

export default DailySleepScreen;
