import React, { useState } from "react";

import { StyleSheet, Text, View } from "react-native";
import DropDownPicker from "react-native-dropdown-picker";

import colors from "../config/colors";
import Screen from "../components/Screen";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import ErrorMessage from "../components/ErrorMessage";
import { ScrollView } from "react-native-gesture-handler";

function isValidInput(category, activeTime, setError) {
  const validCategory = isValidCategory(category);
  const validActiveTime = isValidActiveTime(activeTime);
  setError({ category: !validCategory, activeTime: !validActiveTime });
  return validCategory && validActiveTime;
}

function isNumber(value) {
  return typeof value === "number" && isFinite(value);
}

function isValidActiveTime(activeTime) {
  return isNumber(activeTime) && activeTime > 0;
}

function isValidCategory(category) {
  return category.length > 0;
}

function FitnessEntryFormScreen({ navigation, route }) {
  const initTime = route.params ? route.params.elapsedTime / 1000 / 60 : 0;

  const [category, setCategory] = useState("");
  const [activeTime, setActiveTime] = useState(initTime);
  const [err, setError] = useState({ category: false, activeTime: false });

  const activities = [
    { label: "Cycling", value: "Bicycling: 12-13.9 mph" },
    { label: "Hiking", value: "Hiking: cross country" },
    { label: "Jogging", value: "Running: 6 min/mile" },
    { label: "Sprinting", value: "Running: 10 min/mile" },
    { label: "Swimming", value: "Swimming: laps, vigorous" },
    { label: "Walking", value: "Walk: 15 min/mile" },
    { label: "Weightlifting", value: "Weightlifting: general" },
  ];

  function submit() {
    if (!isValidInput(category, activeTime, setError)) {
      console.log(err);
      return;
    }
    console.log(category, activeTime);
    navigation.popToTop();
  }

  function displayErrorMessage(error) {
    if (error.category) {
      return <ErrorMessage message="Must select a category." />;
    }
    if (error.activeTime) {
      return <ErrorMessage message="Must input a number greater than 0." />;
    }
  }

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 20 }} keyboardShouldPersistTaps="handled">
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
          onChangeItem={(item) => {
            setCategory(item.value);
            setError({ category: false, activeTime: false });
          }}
        />

        <AppText style={styles.text}>How many minutes were you active?</AppText>
        <AppTextInput
          placeholder="30 minutes"
          value={activeTime > 0 ? activeTime.toString() : ""}
          keyboardType="numeric"
          onChangeText={(time) => {
            setActiveTime(Number.parseFloat(time));
            setError({ category: false, activeTime: false });
          }}
        />
        {displayErrorMessage(err)}
        <TextButton
          style={styles.button}
          name="Submit"
          onPress={() => submit()}
        />
      </ScrollView>
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
    backgroundColor: colors.background,
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
