import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet, View } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';

import moment from "moment";
import SummaryItem from '../components/SummaryItem';
import TextButton from '../components/TextButton';
import DailySleepLog from '../components/DailySleepLog';

function DailySleepScreen() {
  const currentDay = getToday();

  return (
    <SafeAreaView>
      <ScrollView alwaysBounceVertical={false} contentContainerStyle={styles.container} >
        <TitleText style={styles.header} children="Today's Sleep Log" />
        <AppText style={styles.dateheader} children={currentDay} />
        <TextButton 
          name={"Add to Sleep Log"}
          onPress={() => console.log("pressed")}
          style={styles.addbutton}
        />
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

        <DailySleepLog 
          style={styles.sleeplog}
          entries={getTodaySleepEntries()}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  addbutton:{
    width: "50%",

  },
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  dateheader: {
    alignSelf: "flex-start",
    marginLeft: "7%",
    marginBottom: 50,
  },
  header: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
    marginBottom: 12,
  },
  sleeplog: {
    marginTop: 25,
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
})

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("MMM Do YYYY");
};

function getTodaySleepEntries() {
  //TODO: change from hardcoded to integration
  const sleepLog = [
    {
      sleeptime: "10:00 pm",
      waketime: "6:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
    {
      sleeptime: "11:00 pm",
      waketime: "8:00 am",
    },
  ];
  return sleepLog;
}

export default DailySleepScreen;