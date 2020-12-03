import React from "react";
import { View, StyleSheet } from "react-native";
import AppText from "./AppText";
import HeaderText from "./HeaderText";
import TitleText from "./TitleText";
import Divider from "./Divider";

function extractNutrientAmountsAndUnits(nutrientAmount) {
  if (nutrientAmount == null) {
    return null;
  }
  if (nutrientAmount > 1) {
    return {
      amount: nutrientAmount ,
      unit: "g",
    };
  } else {
    return {
      amount: nutrientAmount * 1000,
      unit: "mg",
    };
  }
}

function NutritionFacts({ data }) {
  const { label, nutrients } = data;

  const carbAmount = extractNutrientAmountsAndUnits(nutrients.Carbs);
  const fatAmount = extractNutrientAmountsAndUnits(nutrients.Fat);
  const proteinAmount = extractNutrientAmountsAndUnits(nutrients.Protein);
  const fiberAmount = extractNutrientAmountsAndUnits(nutrients.Fiber);

  return (
    <View style={styles.container}>
      <TitleText>Nutrition Facts</TitleText>
      {/* hardcoded 100grams*/}  
      <AppText>{`Serving Size 100g`}</AppText>
      <Divider height={10} />
      <HeaderText>Amount per serving</HeaderText>
      <Divider height={1} />
      <View style={{ flexDirection: "row", justifyContent: "space-between", marginRight: 5 }}>
        <HeaderText>{`Calories `}</HeaderText>
        <HeaderText>{Math.round(nutrients.Cals)}</HeaderText>
      </View>
      <Divider height={5} />
      {fatAmount && (
        <AppText style={styles.text}>{`Fat ${Math.round(fatAmount.amount)}${
          fatAmount.unit
        }`}</AppText>
      )}
      <Divider height={1} />

      {carbAmount && (
        <AppText style={styles.text}>{`Carbohydrate ${Math.round(
          carbAmount.amount
        )}${carbAmount.unit}`}</AppText>
      )}
      <Divider height={1} />

      {proteinAmount && (
        <AppText style={styles.text}>{`Protein ${Math.round(
          proteinAmount.amount
        )}${proteinAmount.unit}`}</AppText>
      )}

      {fiberAmount && (
        <>
          <Divider height={1} />
          <AppText style={styles.text}>{`Fiber ${Math.round(
            fiberAmount.amount
          )}${fiberAmount.unit}`}</AppText>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    borderWidth: 1,
    padding: 15,
    borderRadius: 10,
    marginVertical: 10,
  },
  text: {},
});

export default NutritionFacts;
