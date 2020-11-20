import React from 'react';
import { StyleSheet, Text , View, TouchableOpacity, Dimensions } from 'react-native';
import { AntDesign } from "@expo/vector-icons";


import TitleText from "./TitleText";
import AppText from "./AppText";
import Icon from "./Icon";

function ListItemComponent({title, icon, description, navigation, destination}) {
    return (
      <View style={styles.container}>
          <TouchableOpacity style={styles.titlerow} onPress={() => console.log({destination})}>
            {icon}
            <TitleText style={styles.titletext}>{title}</TitleText>
              <AntDesign style={styles.arrow} name="right" size={24} color="black" />
          </TouchableOpacity>
          <AppText>
            <AppText style={styles.descriptiontext}>
              {description}
            </AppText>
          </AppText>
      </View>
    );
}

const styles = StyleSheet.create({
    arrow: {
      position: "absolute",
      //right: 10,
      right: 10,
      top: 5
    },
    container: {
      flex: 1,
      backgroundColor: '#fff',
      //flexDirection: "row",
      width: Dimensions.get('window').width * .95,
      padding: 7,
      margin: 5,
      borderRadius: 10,
      //alignItems: 'flex-start',
      //justifyContent: 'flex-start',
    },
    descriptiontext: {
      fontSize: 22,
      lineHeight: 30,
      top: 10,
      textAlign: "justify"
    },
    titlerow: {
      flexDirection: "row",
      width: Dimensions.get('window').width * .95,
    },
    titletext: {
      color: "red",
      left: 10,
    },
})

export default ListItemComponent;