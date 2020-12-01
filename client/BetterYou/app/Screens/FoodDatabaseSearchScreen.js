import { useNavigation } from "@react-navigation/native";
import React, { useState } from "react";
import { StyleSheet } from "react-native";
import { ListItem } from "react-native-elements";
import { FlatList, ScrollView } from "react-native-gesture-handler";
import AppTextInput from "../components/AppTextInput";

import Screen from "../components/Screen";
import TextButton from "../components/TextButton";
import colors from "../config/colors";

function FoodDatabaseSearchScreen({ navigation }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  function renderItem({ item }) {
    return (
      <ListItem
        bottomDivider
        onPress={() => {
          console.log("going to form page with " + item.name);
          navigation.navigate("FoodEntryForm", { item: item.name });
        }}
      >
        <ListItem.Content>
          <ListItem.Title>{item.name}</ListItem.Title>
          <ListItem.Subtitle>{item.subtitle}</ListItem.Subtitle>
        </ListItem.Content>
        <ListItem.Chevron />
      </ListItem>
    );
  }

  function keyExtractor(item, index) {
    return index.toString();
  }

  return (
    <Screen style={styles.container}>
      <ScrollView style={{ padding: 20 }}>
        <AppTextInput
          placeholder="Search our database"
          icon="search-web"
          onChangeText={(text) => setQuery(text)}
        />
        <TextButton
          name="Search"
          onPress={() => {
            if (query) {
              console.log(
                `call search api with search query: ${query}, then set results`
              );
              setResults([
                { name: "item1", subtitle: "subtitle1" },
                { name: "item2", subtitle: "subtitle2" },
                { name: "item3", subtitle: "subtitle3" },
                { name: "item4", subtitle: "subtitle4" },
                { name: "item5", subtitle: "subtitle5" },
                { name: "item6", subtitle: "subtitle6" },
                { name: "item7", subtitle: "subtitle7" },
                { name: "item8", subtitle: "subtitle8" },
                { name: "item9", subtitle: "subtitle9" },
                { name: "item10", subtitle: "subtitle10" },
                { name: "item11", subtitle: "subtitle11" },
                { name: "item12", subtitle: "subtitle12" },
                { name: "item13", subtitle: "subtitle13" },
              ]);
            }
          }}
          style={styles.button}
        />
        {results && (
          <FlatList
            keyExtractor={keyExtractor}
            data={results}
            renderItem={renderItem}
          />
        )}
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  button: {
    marginVertical: 10,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
});

export default FoodDatabaseSearchScreen;
