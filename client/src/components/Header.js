import { Link } from "react-router-dom";
import React from "react";

function Header() {
  return (
    <header>
      <h1>
        <Link to="/">Super Heroes</Link>
      </h1>
    </header>
  );
}

export default Header;
