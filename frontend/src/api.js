import axios from "axios";

const API = axios.create({
  baseURL: "https://playto-b8aa.onrender.com",
});

export const getBalance = (id) =>
  API.get(`/api/v1/balance/${id}/`);

export const getPayouts = (id) =>
  API.get(`/api/v1/payouts/${id}/`);

export const getLedger = (id) =>
  API.get(`/api/v1/ledger/${id}/`);

export const createPayout = (data) =>
  API.post(`/api/v1/payouts/`, data, {
    headers: {
      "Idempotency-Key": Date.now().toString(),
    },
  });