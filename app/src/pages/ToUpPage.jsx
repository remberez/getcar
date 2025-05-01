import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const TopUpPage = () => {
  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      // Тут должен быть вызов метода userService.topUpBalance(values.amount)
      console.log("Пополнение на сумму:", values);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto py-12 px-6">
      <h1 className="text-3xl font-bold mb-8 text-center">Пополнение баланса</h1>
      <Formik
        initialValues={{
          amount: "",
          cardNumber: "",
          cardHolder: "",
          expiryDate: "",
          cvc: ""
        }}
        validationSchema={Yup.object({
          amount: Yup.number().min(100, "Минимум 100₽").required("Обязательно"),
          cardNumber: Yup.string()
            .matches(/^\d{16}$/, "Введите 16 цифр")
            .required("Обязательно"),
          cardHolder: Yup.string().required("Обязательно"),
          expiryDate: Yup.string()
            .matches(/^\d{2}\/\d{2}$/, "Формат MM/YY")
            .required("Обязательно"),
          cvc: Yup.string()
            .matches(/^\d{3}$/, "Введите 3 цифры")
            .required("Обязательно"),
        })}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-6 bg-white shadow-md rounded-xl p-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Сумма пополнения (₽)</label>
              <Field name="amount" type="number" className="mt-1 w-full input bg-gray-200 rounded-md p-2" />
              <ErrorMessage name="amount" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Номер карты</label>
              <Field name="cardNumber" type="text" className="mt-1 w-full input bg-gray-200 rounded-md p-2" placeholder="1234 5678 9012 3456" />
              <ErrorMessage name="cardNumber" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Владелец карты</label>
              <Field name="cardHolder" type="text" className="mt-1 w-full input bg-gray-200 rounded-md p-2" placeholder="IVAN IVANOV" />
              <ErrorMessage name="cardHolder" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Срок действия</label>
                <Field name="expiryDate" type="text" className="mt-1 w-full input bg-gray-200 rounded-md p-2" placeholder="MM/YY" />
                <ErrorMessage name="expiryDate" component="div" className="text-red-600 text-sm mt-1" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">CVC</label>
                <Field name="cvc" type="password" className="mt-1 w-full input bg-gray-200 rounded-md p-2" placeholder="123" />
                <ErrorMessage name="cvc" component="div" className="text-red-600 text-sm mt-1" />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-red-600 text-white py-2 rounded-md hover:bg-red-700 transition"
            >
              {isSubmitting ? "Обработка..." : "Пополнить баланс"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default TopUpPage;
