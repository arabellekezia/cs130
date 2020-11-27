import React, { useState } from "react";

import { StyleSheet, Text, View } from "react-native";
import DropDownPicker from "react-native-dropdown-picker";

import colors from "../config/colors";
import Screen from "../components/Screen";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";

function FitnessEntryFormScreen() {
  const [category, setCategory] = useState("");
  const [activeTime, setActiveTime] = useState(0);
  const activities = [
    { label: "Cycling", value: "Bicycling: 12-13.9 mph" },
    { label: "Hiking", value: "Hiking: cross country" },
    { label: "Jogging", value: "Running: 6 min/mile" },
    { label: "Sprinting", value: "Running: 10 min/mile" },
    { label: "Swimming", value: "Swimming: laps, vigorous" },
    { label: "Walking", value: "Walk: 15 min/mile" },
    { label: "Weightlifting", value: "Weightlifting: general" },
  ];

  return (
    <Screen style={styles.container}>
      <View style={{ padding: 10 }}>
        <AppText style={styles.text}>What activity did you do?</AppText>

        <DropDownPicker
          defaultNull
          placeholder="Select an item"
          items={activities}
          containerStyle={{ height: 40 }}
          style={styles.dropdownInner}
          labelStyle={{ fontSize: 18, color: colors.dark }}
          containerStyle={styles.dropDownContainer}
          placeholderStyle={styles.dropDownPlaceholder}
          dropDownStyle={styles.dropDownList}
          onChangeItem={(item) => setCategory(item.value)}
        />
        <AppText style={styles.text}>How many minutes were you active?</AppText>
        <AppTextInput
          placeholder="30 minutes"
          keyboardType="numeric"
          onChangeText={(activeTime) => setActiveTime(activeTime)}
        />
        <TextButton
          style={styles.button}
          name="Submit"
          onPress={() => console.log(category, activeTime)}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  button: {
    marginVertical: "5%",
  },
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: colors.primary,
  },
  dropDownContainer: {
    height: 50,
    marginTop: 10,
  },
  dropdownInner: {
    backgroundColor: "#efefef",
  },
  dropDownLabels: {
    fontSize: 18,
    color: colors.dark,
  },
  dropDownList: {
    backgroundColor: "#fafafa",
  },
  dropDownPlaceholder: {
    color: "#7e7e7e",
  },
  text: {
    marginTop: "5%",
    fontSize: 16,
  },
});

export default FitnessEntryFormScreen;
