import React from 'react';
import { StyleSheet, Text , View, TouchableOpacity, Dimensions } from 'react-native';
import { AntDesign } from "@expo/vector-icons";


//import TitleText from "./TitleText";
import AppText from "./AppText";
import HeaderText from './HeaderText';
//import Icon from "./Icon";

function ListItemComponent({title, icon, description, navigation, destination}) {
    return (
      <TouchableOpacity
        style={styles.container}
        onPress={() => console.log({ destination })}
      >
        <View style={styles.titlerow}> 
          {icon}
          <View style={styles.dayOfWeekContainer}> 
            <HeaderText style={styles.headertext}>{title}</HeaderText>
          </View>
          <View style={styles.arrowContainer}> 
            <AntDesign
              name="right"
              size={24}
              color="black"
            />
          </View>
        </View>
        <AppText>
          <AppText style={styles.descriptiontext}>{description}</AppText>
        </AppText>
      </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
  arrowContainer: {
    flex: 1, 
    flexDirection: "row", 
    justifyContent: "flex-end", 
   }, 
  container: {
    width: Dimensions.get("window").width * 0.9,
    marginLeft: 20,
    marginBottom: 20,
    padding: 12,
    paddingHorizontal: 12,
    borderRadius: 10,
    alignItems: 'flex-start',
    justifyContent: 'center',
    borderWidth: 1
  },
  descriptiontext: {
    fontSize: 15,
    lineHeight: 30,
    top: 10,
    textAlign: "justify",
    color: "#474747"  
  },
  titlerow: {
    flexDirection: "row",
    justifyContent: "space-between", 
    alignItems: 'center',
  },
  dayOfWeekContainer: {
    flex: 1, 
    flexDirection: "row", 
    justifyContent: "flex-start"
  }, 
  headertext: {
    color: "black"  
  },
});

export default ListItemComponent;