import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";

import { groupBy } from "lodash";

import AppText from "../components/AppText";
import TitleText from "../components/TitleText";

import moment from "moment";
import { useIsFocused } from "@react-navigation/native";
import DailySleepEntries from "../components/DailySleepEntries";
import SleepService from "../services/SleepService";


function DailySleepScreen({ route }) {
  const [isReady, setReady] = useState(false);
  const [sleepEntries, setSleepEntries] = useState({ sleep: [], naps: [] });

  const date = route.params ? route.params.date : Date.now();

  const isFocused = useIsFocused();

  useEffect(() => {
    let mounted = true;

    loadSleepEntries().then(() => {
      if (mounted) {
        setReady(true);
      }
    });

    return function cleanup() {
      mounted = false;
    };
  }, [isFocused]);

  const loadSleepEntries = async () => {
    setReady(false);
    const entries = await getTodaySleepEntries(date);
    setSleepEntries(entries);
    //setReady(true);
  };

  return (
    <SafeAreaView>
      {!isReady && (
        <ActivityIndicator animating={!isReady} size="large" color="#343434" />
      )}
      {isReady && (
        <ScrollView
          alwaysBounceVertical={false}
          contentContainerStyle={styles.container}
        >
          <TitleText style={styles.pageTitle} children="Sleep" />
          <AppText style={styles.dateHeader} children={getToday(date)} />

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


function getToday(date) {
  return moment(date).format("dddd, MMMM Do");
}


async function getTodaySleepEntries(date) {
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
