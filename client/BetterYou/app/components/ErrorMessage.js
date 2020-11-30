import React from "react";
import AppText from "./AppText";

function ErrorMessage({ message }) {
  return (
    <AppText
      style={{
        alignSelf: "flex-start",
        marginLeft: "6%",
        color: "red",
      }}
    >
      {message}
    </AppText>
  );
}

export default ErrorMessage;
