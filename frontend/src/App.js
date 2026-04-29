import { useEffect, useState } from "react";
import { getBalance, getPayouts, createPayout } from "./api";

function App() {
  const merchantId = 1;

  const [available, setAvailable] = useState(0);
  const [held, setHeld] = useState(0);
  const [payouts, setPayouts] = useState([]);
  const [amount, setAmount] = useState("");

  const fetchData = async () => {
    const b = await getBalance(merchantId);
    const p = await getPayouts(merchantId);

    setAvailable(b.data.available_balance);
    setHeld(b.data.held_balance);
    setPayouts(p.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePayout = async () => {
    if (!amount) return;

    await createPayout({
      merchant_id: merchantId,
      amount_paise: Number(amount),   // ✅ FIX
      bank_account_id: "demo_account_1", // ✅ FIX
    });

    setAmount("");
    setTimeout(fetchData, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6">
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">💳 Playto Dashboard</h1>
          <span className="text-sm text-gray-300">Merchant #1</span>
        </div>

        {/* Balance Card */}
       <div className="grid grid-cols-2 gap-4 mt-4">
  <div>
    <p className="text-gray-300 text-sm">Available</p>
    <h2 className="text-2xl text-green-400 font-bold">
      ₹ {available}
    </h2>
  </div>

  <div>
    <p className="text-gray-300 text-sm">Held</p>
    <h2 className="text-2xl text-yellow-400 font-bold">
      ₹ {held}
    </h2>
  </div>
</div>

        {/* Payout Form */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg border border-white/10">
          <h2 className="text-xl font-semibold mb-4">Request Payout</h2>

          <div className="flex gap-3">
            <input
              type="number"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="flex-1 px-4 py-2 rounded-lg bg-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-blue-400"
            />

            <button
              onClick={handlePayout}   // ✅ FIX
              className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-2 rounded-lg font-semibold hover:scale-105 transition"
            >
              Send
            </button>
          </div>
        </div>

        {/* Payout History */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg border border-white/10">
          <h2 className="text-xl font-semibold mb-4">Payout History</h2>

          <div className="overflow-hidden rounded-lg">
            <table className="w-full text-sm">
              <thead className="bg-white/10 text-gray-300">
                <tr>
                  <th className="p-3 text-left">ID</th>
                  <th className="p-3 text-left">Amount</th>
                  <th className="p-3 text-left">Status</th>
                </tr>
              </thead>

              <tbody>
                {payouts.map((p) => (
                  <tr key={p.id} className="border-b border-white/10 hover:bg-white/5">
                    <td className="p-3">{p.id}</td>
                    <td className="p-3">₹ {p.amount}</td>
                    <td className="p-3">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold
                        ${
                          p.status === "SUCCESS"
                            ? "bg-green-500/20 text-green-400"
                            : p.status === "FAILED"
                            ? "bg-red-500/20 text-red-400"
                            : "bg-yellow-500/20 text-yellow-300"
                        }`}
                      >
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;