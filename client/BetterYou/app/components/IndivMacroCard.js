import React from "react";
import Icon from "./Icon";
import { StyleSheet, View, Text, Dimensions } from "react-native";
import AppText from "./AppText";
import HeaderText from "./HeaderText";

/**
 * This function produces a visual component that organizes and displays a component displaying stats 
 * about a single macronutrient in a visually appealing way
 * @module
 * @param { Object } ParameterObj The Object that encompasses all the parameters
 * @param {StyleSheet} ParameterObj.style Possible Additional stylesheet (optional)
 * @param {string} ParameterObj.macroName name of the macronutrient (Carbs, Protein. Fat)
 * @param {number} ParameterObj.percentage percentage of the macronutrient in the user's diet for the day
 * @param {Object} ParameterObj.foods Object that pairs the food name with the amount of a certain macronutrient in grams
 * @returns {View} A View that contains everything to be displayed with the parameters filling in the details
 */
function IndivMacroCard({
  style,
  macroName,
  percentage,
  foods,
}) {
  return (
    <View style={{ ...styles.container, ...style }}>
      
      <View style={styles.header}>
        <HeaderText style={styles.headertext} children={macroName} />
        <AppText style={styles.percentagetext}>
          <AppText style={styles.boldtext} children={ `${percentage} `} />
          of your diet today was {macroName}
        </AppText>
      </View>
      
        
      <View style={styles.headerunderline} />
      
      <View style={styles.foodcontainer}>
        {foodList(foods)}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  boldtext: {
    fontWeight: "bold",
  },
  container: {
    justifyContent: "center",
    alignItems: "center",
    width: Dimensions.get("window").width * 0.9,
    paddingVertical: 6, 
    paddingHorizontal: 12, 
  },
  header: {
    paddingLeft: 4,
    width: "100%",
  },
  headertext: {
    marginVertical: 10,
  },
  foodcontainer: {
    justifyContent: "center",
  },
  foodname: {
    // width: Dimensions.get('window').width * .65,
    width: "90%",
  },
  foodstats: {
    flexDirection: "row",
    justifyContent: "space-between",
    //width: Dimensions.get('window').width * .80,
    //width: "80%",
    paddingBottom: 10,
    // paddingLeft: 5,
    paddingHorizontal: 8,
  },
  headerunderline: {
    marginVertical: 15,
    borderBottomColor: "#dddddd",
    borderBottomWidth: 1,
    width: "100%",
  },
  percentagetext: {
    //marginBottom: 10,
  },
  rowContainer: {
    flexDirection: "row",
    justifyContent: "flex-start",
  },
});


function foodList(foodList) {
  //based on hard coding, this loop would most likely need to be fixed later
  return foodList.foodarray.map((element, key) => {
    return (
      <View key={key} style={styles.foodstats}>
        <Text style={styles.foodname} numberOfLines={1} >{element.name.charAt(0).toUpperCase() + element.name.slice(1)}</Text>
        <AppText children={`${element.grams}g`} />
      </View>
    );
  });
};

export default IndivMacroCard;
