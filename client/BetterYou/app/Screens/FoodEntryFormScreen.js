import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import NutritionFacts from "../components/NutritionFacts";

import Screen from "../components/Screen";
import TextButton from "../components/TextButton";
import TitleText from "../components/TitleText";
import ErrorMessage from "../components/ErrorMessage";
import colors from "../config/colors";
import { ScrollView } from "react-native-gesture-handler";

function isValidInput(numberOfServings, setError) {
  const validNumber = isNumber(numberOfServings) && numberOfServings > 0;
  setError({ numberOfServings: !validNumber });
  return validNumber;
}

function isNumber(value) {
  return typeof value === "number" && isFinite(value);
}
// TO DO: replace params from label.. do api call to get the name instead
function FoodEntryFormScreen({ navigation, route }) {
  const [numberOfServings, setNumberOfServings] = useState(0);
  const [err, setError] = useState({ numberOfServings: false });

  function submit() {
    if (!isValidInput(numberOfServings, setError)) {
      console.log(err);
      // setError({ numberOfServings: true });
      return;
    }
    console.log(`post number of servings to endpoint ${numberOfServings}`);
    navigation.popToTop();
  }

  function displayErrorMessage(error) {
    if (error.numberOfServings) {
      return <ErrorMessage message="Must be a number greater than 0." />;
    }
  }

  const nutritionData = {
    label: "Jamba Juice Orange Carrot Karma Smoothie",
    servingSize: "22 fl oz",
    nutrients: {
      calories: 41.499027861352765,
      protein: 0.6148004127607817,
      fat: 0.15370010319019542,
      carbohydrates: 10.144206810552898,
      fiber: 0.6148004127607817,
    },
  };

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 10 }} keyboardShouldPersistTaps="handled">
        <TitleText style={styles.header}>{route.params.item}</TitleText>
        <NutritionFacts data={nutritionData} />
        <AppText style={styles.text}>How many servings did you eat?</AppText>
        <AppTextInput
          placeholder="1 serving"
          keyboardType="numeric"
          onChangeText={(text) => {
            setNumberOfServings(Number.parseFloat(text));
            setError({ numberOfServings: false });
          }}
        />
        {displayErrorMessage(err)}
        <TextButton
          style={styles.textButton}
          name="Submit"
          onPress={() => {
            submit();
          }}
        />
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    marginBottom: 10,
  },
  text: {
    fontSize: 16,
  },
  textButton: {
    marginTop: 10,
  },
});

export default FoodEntryFormScreen;
