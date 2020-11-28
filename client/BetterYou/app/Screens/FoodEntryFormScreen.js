import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import HeaderText from "../components/HeaderText";

import Screen from "../components/Screen";
import TextButton from "../components/TextButton";
import colors from "../config/colors";

function FoodEntryFormScreen() {
  const [numberOfServings, setNumberOfServings] = useState(0);

  const selectedFood = "Chicken Casserole";
  // TO DO: add nutrition label or similar component (incl food serving sizes at min)
  return (
    <Screen>
      <View style={{ padding: 10 }}>
        <HeaderText style={styles.header}>{selectedFood}</HeaderText>
        <AppText style={styles.text}>How many servings did you eat?</AppText>
        <AppTextInput
          placeholder="1 serving"
          keyboardType="numeric"
          onChangeText={(text) => setNumberOfServings(text)}
        />
        <TextButton
          name="Submit"
          onPress={() => {
            console.log(numberOfServings);
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
