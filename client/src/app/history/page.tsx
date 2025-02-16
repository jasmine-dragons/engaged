import { HistoryItem } from "@/components/HistoryItem";
import { getHistory } from "@/lib/api";

const USER_ID = "2";

export default async function History() {
  const { data } = await getHistory(USER_ID);
  return (
    <div className="container">
      <h1 className="heading">Past Sessions</h1>
      {data
        .toSorted((a, b) => b.timestamp.localeCompare(a.timestamp))
        .map((anal, i) => (
          <HistoryItem
            analysis={anal}
            key={anal.timestamp}
            style={{ animationDelay: `${i * 50}ms` }}
          />
        ))}
    </div>
  );
}
