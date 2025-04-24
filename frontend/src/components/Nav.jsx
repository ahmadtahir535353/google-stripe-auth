import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Nav() {
  const [user, setUser] = useState({});
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    let user = localStorage.getItem("user");
    setUser(JSON.parse(user));
    axios
      .get(`${import.meta.env.VITE_BACKEND_URL}/auth/user`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => {
        console.log(res);
        setUser(res.data);
        localStorage.setItem("user", JSON.stringify(res.data));
      })
      .catch((err) => {
        console.log(err);
        if (err.status == 401) {
          localStorage.clear();
          navigate("/login");
        }
      })
      .finally(() => { });
  }, []);
  
  const decodeProfilePictureUrl = (encodedUrl) => {

    // Decode the URL
    let decodedUrl = decodeURIComponent(encodedUrl);
    // Check if the URL starts with '/https:'
    if (decodedUrl.startsWith('/https:')) {
      // Remove the leading '/' and decode the rest
      decodedUrl = decodedUrl.slice(1);  // Removes the '/'
    }


    return decodedUrl;
  }

  const logout = () => {
    axios
      .post(`${import.meta.env.VITE_BACKEND_URL}/auth/logout`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => {
        localStorage.clear();
        navigate("/login");
        console.log(res);
      })
      .catch((err) => {
        if (err.status == 401) {
          localStorage.clear();
          navigate("/login");
        }
      });
  };
  return (
    <>
      <nav className="bg-gray-200 shadow shadow-gray-300 w-100 px-8 md:px-auto">
        <div className="md:h-16 h-28 mx-auto md:px-4 container flex items-center justify-between flex-wrap md:flex-nowrap">
          <div className="text-indigo-500 md:w-32 md:order-1">
            <Link to="/">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-10 w-10"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                />
              </svg>
            </Link>
          </div>
          <div className="text-gray-500 order-3 w-full md:w-auto md:order-2">
            <ul className="flex font-semibold justify-between">
              <li className="md:px-4 md:py-2 text-indigo-500">
                <Link to="/">Home</Link>
              </li>
              <li className="md:px-4 md:py-2 hover:text-indigo-400">
                <Link to="/about">About</Link>
              </li>
              <li className="md:px-4 md:py-2 hover:text-indigo-400">
                <Link to="/services">Services</Link>
              </li>
              <li className="md:px-4 md:py-2 hover:text-indigo-400">
                <Link to="/contact">Contact</Link>
              </li>
            </ul>
          </div>
          <div className="flex items-center gap-3 order-2 md:order-3">
            <button className={`px-4 py-2 ${user.is_subscribed ? "bg-indigo-500" : "bg-transparent"}  hover:bg-indigo-600 text-gray-50 rounded-xl flex items-center gap-2`}>
              <span>{user?.is_subscribed ? "Subscribed" : "Subscribe"}</span>
            </button>

            {/* Dropdown */}
            <div className="relative inline-block text-left">
              <div>
                <button
                  type="button"
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                >
                  <img
                    className="w-8 h-8 rounded-full"
                    src={
                      user?.profile_picture
                        ? decodeProfilePictureUrl(user.profile_picture)
                        : "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png?20150327203541"
                    }
                    alt="user photo"
                  />
                </button>
              </div>
              <div
                className={`absolute right-0 z-10 mt-2 w-56 ${isDropdownOpen ? "max-h-[500px] visible" : "max-h-0 invisible"
                  } overflow-hidden origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none`}
              >
                <div role="none">
                  <Link
                    to="/contact"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 transition-all"
                  >
                    Contact Us
                  </Link>
                  <Link
                    to="/about"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 transition-all"
                  >
                    About
                  </Link>
                  <button
                    type="submit"
                    className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-200 transition-all"
                    onClick={logout}
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
}

export default Nav;
