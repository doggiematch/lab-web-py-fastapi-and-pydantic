import { useFetch } from "../hooks/useFetch";

const PublicGists = () => {
  const {
    data: gists,
    loading,
    error,
  } = useFetch("https://api.github.com/gists/public");
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error</p>;
  return (
    <div>
      <h2>Public Gists</h2>
      <ul>
        {gists.map((gist) => (
          <li key={gist.id}>
            <a href={gist.html_url}>{gist.description || "No description"}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PublicGists;
