import React from "react";
import { Navigate } from "react-router-dom";

const SubscribedRoute = ({ children }: any) => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  return user.is_subscribed ? children : <Navigate to="/home" />;
};

export default SubscribedRoute;
