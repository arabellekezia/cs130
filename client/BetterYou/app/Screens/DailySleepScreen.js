import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet, View } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';

import moment from "moment";
import TextButton from '../components/TextButton';
import DailySleepEntries from "../components/DailySleepEntries";

function DailySleepScreen() {
  const currentDay = getToday();

  return (
    <SafeAreaView>
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Sleep" />
        <AppText style={styles.dateHeader} children={currentDay} />
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
          entries={[getTodaySleepEntries().sleep]}
        />

        <DailySleepEntries
          style={styles.sleepLog}
          headerTextStyle={styles.sleepEntryHeader}
          headerText="Recorded naps"
          entries={getTodaySleepEntries().naps}
        />
      </ScrollView>
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
    marginBottom: 12,
  },
  sleepLog: {
    marginTop: 12,
  },
  sleepEntryHeader: {
    marginLeft: "5%" 
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

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("dddd, MMMM Do");
};

function getTodaySleepEntries() {
  //TODO: change from hardcoded to integration
  /* Note from evan - backend allows us to differentiate between naps + actual sleep, so i'm using that info */
  return {
    sleep: {
      sleeptime: "10:00 pm",
      waketime: "6:00 am",
    }, 
    naps: [
      {
        sleeptime: "11:00 pm",
        waketime: "8:00 am",
      },
      {
        sleeptime: "11:00 pm",
        waketime: "8:00 am",
      },
    ]
  };
}

export default DailySleepScreen;