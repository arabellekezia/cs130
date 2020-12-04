import { useNavigation } from "@react-navigation/native";
import React, { useState } from "react";
import { ActivityIndicator, StyleSheet } from "react-native";
import { ListItem } from "react-native-elements";
import { FlatList, ScrollView } from "react-native-gesture-handler";
import AppTextInput from "../components/AppTextInput";

import Screen from "../components/Screen";
import TextButton from "../components/TextButton";
import colors from "../config/colors";

import NutritionService from "../services/NutritionService";

function FoodDatabaseSearchScreen({ navigation }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);

  function renderItem({ item }) {
    return (
      <ListItem
        bottomDivider
        onPress={() => {
          console.log("going to form page with " + item.name);
          navigation.navigate("FoodEntryForm", {
            item: item.name,
            barcode: "false",
            data: item.nutrition,
          });
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
          onPress={async () => {
            if (query) {
              // upon pressing the search button and query is sent and fetched
              setSearching(true);
              const entries = await getListOfFoods(query);
              setSearching(false);
              console.log(
                `call search api with search query: ${query}, then set results`
              );
              setResults(entries);
            }
          }}
          style={styles.button}
        />
        {searching && (
          <ActivityIndicator animating={true} size="large" color="#343434" />
        )}
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

async function getListOfFoods(searchquery) {
  try {
    const foodList = await NutritionService.getAvailableFoods(
      searchquery,
      15,
      1
    );
    const parsedList = pairItemNameAndCalories(foodList);

    return parsedList;
  } catch (err) {
    console.log(err);
  }
}

function pairItemNameAndCalories(list) {
  const pairList = [];
  //const calsList = [];
  for (const index in list) {
    const itemPair = {
      name: list[index].Label,
      subtitle:
        list[index].Nutrients.Cals !== undefined
          ? `${Math.round(list[index].Nutrients.Cals)} Cals per 100g ` //added rounding to cals
          : "",
      nutrition: list[index].Nutrients, //passing this so the entry form screen doesn't have to make another call
    };
    pairList.push(itemPair);
  }
  return pairList;
}

export default FoodDatabaseSearchScreen;
