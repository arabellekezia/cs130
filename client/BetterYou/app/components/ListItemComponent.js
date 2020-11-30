import React from 'react';
import { StyleSheet, Text , View, TouchableOpacity, Dimensions } from 'react-native';
import { AntDesign } from "@expo/vector-icons";


//import TitleText from "./TitleText";
import AppText from "./AppText";
import HeaderText from './HeaderText';
//import Icon from "./Icon";

function ListItemComponent({title, icon, description, descriptionStyle, children, navigation, destination}) {
    return (
      <TouchableOpacity
        style={styles.container}
        onPress={() => console.log({ destination })}
      >
        <View style={styles.titlerow}> 
          <View style={styles.dayOfWeekContainer}> 
            <HeaderText style={styles.headertext}>{title}</HeaderText>
            {icon}         
          </View>
          <View style={styles.arrowContainer}> 
            <AntDesign
              name="right"
              size={24}
              color="black"
            />
          </View>
        </View>
        <AppText style={{...styles.descriptiontext, ...descriptionStyle}}>{description}</AppText>
        {children}
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
    lineHeight: 20,
    color: "#474747",
    marginVertical: 6 
  },
  titlerow: {
    flexDirection: "row",
    justifyContent: "space-between", 
    alignItems: 'center',
  },
  dayOfWeekContainer: {
    flex: 1, 
    flexDirection: "row", 
    justifyContent: "flex-start",
    alignItems: "center"
  }, 
  headertext: {
    color: "black", 
    marginRight: 2
  },
});

export default ListItemComponent;