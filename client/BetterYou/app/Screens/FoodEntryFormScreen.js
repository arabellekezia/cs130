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

import NutritionService from "../services/NutritionService";


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

  const nutritionData = {
    label: route.params.item,
    nutrients: route.params.data,
  };

  async function submit() {
    if (!isValidInput(numberOfServings, setError)) {
      console.log(err);
      // setError({ numberOfServings: true });
      return;
    }
    console.log(`post number of servings to endpoint ${numberOfServings}`);
    try {
      await NutritionService.addMeals(
        route.params.barcode === "true" ? route.params.barcodenum : route.params.item,
        numberOfServings,
        route.params.barcode,
      );
      navigation.popToTop();
    } catch (error) {
      console.log(error);
    }
  }

  function displayErrorMessage(error) {
    if (error.numberOfServings) {
      return <ErrorMessage message="Must be a number greater than 0." />;
    }
  }

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 20 }} keyboardShouldPersistTaps="handled">
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
          onPress={async () => {
            await submit();
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
