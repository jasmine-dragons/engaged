import styles from "./page.module.css";

export default function Login() {
  return (
    <form className={styles.page} action="/setup">
      <h1 className="heading">Welcome.</h1>
      <label className={styles.label}>
        <span>Email</span>
        <input type="email" placeholder="you@example.com" />
      </label>
      <label className={styles.label}>
        <span>Password</span>
        <input type="password" placeholder="••••••••" />
      </label>
      <button type="submit" className="button">
        Log In
      </button>
    </form>
  );
}
