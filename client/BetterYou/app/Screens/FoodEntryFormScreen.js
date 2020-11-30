import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import NutritionFacts from "../components/NutritionFacts";

import Screen from "../components/Screen";
import TextButton from "../components/TextButton";
import TitleText from "../components/TitleText";
import colors from "../config/colors";

function FoodEntryFormScreen() {
  const [numberOfServings, setNumberOfServings] = useState(0);

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
    <Screen>
      <View style={{ padding: 10 }}>
        <TitleText style={styles.header}>{nutritionData.label}</TitleText>
        <NutritionFacts data={nutritionData} />
        <AppText style={styles.text}>How many servings did you eat?</AppText>
        <AppTextInput
          placeholder="1 serving"
          keyboardType="numeric"
          onChangeText={(text) => setNumberOfServings(text)}
        />
        <TextButton
          name="Submit"
          onPress={() => {
            console.log(
              `post number of servings to endpoint ${numberOfServings}`
            );
          }}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.primary,
  },
  header: {
    marginBottom: 10,
  },
  text: {
    fontSize: 16,
  },
});

export default FoodEntryFormScreen;
