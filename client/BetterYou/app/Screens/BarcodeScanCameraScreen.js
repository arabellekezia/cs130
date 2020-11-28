import React, { useEffect, useState } from "react";

import { View, Text } from "react-native";
import { Camera } from "expo-camera";
import { TouchableOpacity } from "react-native-gesture-handler";
import { MaterialCommunityIcons } from "@expo/vector-icons";

function BarcodeScanCameraScreen() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const handleBarCodeScanned = ({ type, data }) => {
    setScanned(true);
    // to do: make api call, then redirect to confirmation screen with results as parameters
    alert(
      `Bar code with type ${type} and data ${data} has been scanned!... redirecting you to confirmation screen`
    );
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }
  return (
    <View style={{ flex: 1 }}>
      <Camera
        style={{ flex: 1 }}
        type={Camera.Constants.Type.back}
        autoFocus="on"
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
      >
        <View></View>

        <View
          style={{
            flex: 1,
            justifyContent: "flex-end",
            backgroundColor: "transparent",
            paddingBottom: 40,
          }}
        >
          <View
            style={{
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <TouchableOpacity
              style={{ marginHorizontal: 30 }}
              onPress={() =>
                console.log("navigate back to input type selection screen")
              }
            >
              <MaterialCommunityIcons
                name="window-close"
                color="#fff"
                size={40}
              />
            </TouchableOpacity>
          </View>
        </View>
      </Camera>
    </View>
  );
}

export default BarcodeScanCameraScreen;
