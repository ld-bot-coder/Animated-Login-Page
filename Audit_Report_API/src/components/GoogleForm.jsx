import React, { useState } from "react";
import axios from "axios";
import logo from "../assets/logo.png"

function GoogleForm() {
  const [formData, setFormData] = useState({
    name: "",
    pincode: "",
    phone: "",
    speciality: "",
    area: "",
    city: "",
    state: "",
    country: "",
    gmb_link: "",
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePincodeChange = async (e) => {
    const pincode = e.target.value;
    setFormData((prev) => ({ ...prev, pincode }));

    if (pincode.length === 6) {
      try {
        const response = await axios.get(`https://api.postalpincode.in/pincode/${pincode}`);
        const data = response.data[0];

        if (data.Status === "Success" && data.PostOffice && data.PostOffice.length > 0) {
          const locationInfo = data.PostOffice[0];
          setFormData((prev) => ({
            ...prev,
            city: locationInfo.District,
            state: locationInfo.State,
            country: locationInfo.Country,
          }));
        } else {
          alert("Invalid pincode or no data available.");
        }
      } catch (error) {
        console.error("Error fetching pincode data", error);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "https://staging.multipliersolutions.com/Audit_Report_API/submit_form.php",
        formData
      );
      if (response.data) {
        setSubmitted(true);
      }
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('https://s3-alpha-sig.figma.com/img/3bea/8a87/26fbf8711df83b40ea54d869a307e803?Expires=1726444800&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=NaE~qi3qYEJclwwsz9qIJHthQzSYMfkhzV6DGueNkt0WDMLvjmPKGCYDZnmroIfT3lQ3NATati2RXlE3qFX16Pb2EDgS7PEDHxwFX-xRerNY4Nc7IYkDSy-KngKKJqMbcB3U8lwXgyeJ15eOacbuAEwc3WBY2XBtpp9L1QKfNL5Ccydlxukgb2Uvg2xINTlCNqcbQHGUJ6Iu79ErMAzf2Z7hb0EjtuOjiItAG88pv-swew4AQ13L65PFa2Qy02cAB0Z80TUhnFB2XB-ljf30jchEVabYS~9mGp545ve1SyQFFlDVDldvcXdJuux3QX4-EuVlF7lQ0ree65nQx60VcQ__')" }} // add your background image URL here
    >
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-xl mt-5">
        <div className="mb-6 text-center">
          <img
            src={logo}
            alt="Logo"
            className="h-16 mx-auto"
          />
          <h1 className="text-2xl font-semibold mt-2">Fill The Form</h1>
        </div>

        {/* Add the provided text above the form */}
        <div className="mb-4 text-gray-700 text-center">
          <p className="font-semibold">
            Google listing e-registration
          </p>
          <p>
            Please fill the form below to set up your Google My Business listing.In case of any help or support required, please call/WhatsApp us at:{" "}
            <a href="tel:7337063737" className="text-blue-500 font-semibold">
              7337063737
            </a>
          </p>
          <p className="mt-2 text-sm italic">
            Disclaimer: Identifying information collected is for registration purposes and shall be used for the making of your Google My Business Profile only.
          </p>
        </div>

        {submitted ? (
          <div className="text-center text-green-600 text-lg">
            Form submitted successfully!
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Name
              </label>
              <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                type="text"
                placeholder="Enter your name"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Pincode
              </label>
              <input
                name="pincode"
                value={formData.pincode}
                onChange={handlePincodeChange}
                type="text"
                placeholder="Enter pincode"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Phone
              </label>
              <input
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                type="text"
                placeholder="Enter phone number"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Speciality
              </label>
              <input
                name="speciality"
                value={formData.speciality}
                onChange={handleChange}
                type="text"
                placeholder="Enter speciality"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Area
              </label>
              <input
                name="area"
                value={formData.area}
                onChange={handleChange}
                type="text"
                placeholder="Enter area"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                City
              </label>
              <input
                name="city"
                value={formData.city}
                onChange={handleChange}
                type="text"
                placeholder="City will be filled automatically"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
                readOnly
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                State
              </label>
              <input
                name="state"
                value={formData.state}
                onChange={handleChange}
                type="text"
                placeholder="State will be filled automatically"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
                readOnly
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Country
              </label>
              <input
                name="country"
                value={formData.country}
                onChange={handleChange}
                type="text"
                placeholder="Country will be filled automatically"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
                readOnly
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                GMB Link (Optional)
              </label>
              <input
                name="gmb_link"
                value={formData.gmb_link}
                onChange={handleChange}
                type="text"
                placeholder="Enter GMB link (Optional)"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>

            <div className="flex items-center justify-between">
              <button
                type="submit"
                className="bg-[#7C3A84] hover:bg-[#5A2962] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Submit
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default GoogleForm;
