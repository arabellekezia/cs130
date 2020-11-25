import React, { useEffect, useRef } from "react";

import { TextInput, View, StyleSheet } from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

function AppTextInput({ style, icon, isError = false, ...kwargs }) {
  // Workaround to get the correct font-family after using a secure text entry for password field
  const inputElementRef = useRef(null);
  useEffect(() => {
    inputElementRef.current.setNativeProps({
      style: {
        fontFamily: Platform.OS === "android" ? "Roboto" : "San Francisco",
      },
    });
  }, []);
  
  const [backgroundColor, setBackgroundColor] = React.useState("#efefef");
  
  const styles = StyleSheet.create({
    container: Object.assign({
      backgroundColor,
      borderRadius: 10,
      width: "100%",
      flexDirection: "row",
      padding: 15,
      marginVertical: 10,
    }, 
      isError ? { borderWidth: 1} : null, 
      isError ? { borderColor: "red"} : null
    ), 
    icon: {
      marginRight: 14,
    },
    textInput: {
      fontSize: 18,
    },
  });

  return (
    <View style={{  ...styles.container, ...style }}>
      {icon && (
        <MaterialCommunityIcons
          name={icon}
          color="#7e7e7e"
          size={26}
          style={styles.icon}
        />
      )}
      <TextInput {...kwargs} onFocus={() => setBackgroundColor("#f7f7f7")} onBlur={() => setBackgroundColor("#efefef")} ref={inputElementRef}
        style={styles.textInput}
      />
    </View>
  );
}


export default AppTextInput;
