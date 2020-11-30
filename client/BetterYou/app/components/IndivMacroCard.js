import React from "react";
import Icon from "./Icon";
import { StyleSheet, View, Text, Dimensions } from "react-native";
import AppText from "./AppText";
import HeaderText from "./HeaderText";

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
    width: Dimensions.get('window').width * .85,
  },
  header: {
    paddingLeft: 7,
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
  foodstats:{
    flexDirection: "row",
    justifyContent: "space-between",
    //width: Dimensions.get('window').width * .80,
    //width: "80%",
    paddingBottom: 10,
    //paddingLeft: 5,
    paddingHorizontal: 5,
  },
  headerunderline: {
    marginVertical: 15,
    borderBottomColor: "#dddddd",
    borderBottomWidth: 1,
    width: "95%",
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
        <Text style={styles.foodname} numberOfLines={1} >{element.name}</Text>
        <AppText children={`${element.grams}g`} />
      </View>
    );
  });
};

export default IndivMacroCard;
