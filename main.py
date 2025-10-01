import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("Personal Finance Tracker")


if not os.path.exists('transactions.csv'):
    pd.DataFrame(columns=['date', 'type', 'category', 'amount', 'description']).to_csv('transactions.csv', index=False)


df = pd.read_csv('transactions.csv')


st.sidebar.header("➕ Add New Transaction")


trans_type = st.sidebar.selectbox("Type", ["Income", "Expense"])


if trans_type == "Income":
    category = st.sidebar.selectbox("Category",
                                    ["Salary", "Freelance", "Investment", "Gift", "Other Income"])
else:
    category = st.sidebar.selectbox("Category",
                                    ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Healthcare",
                                     "Utilities"])

amount = st.sidebar.number_input("Amount ($)", min_value=0.0, step=0.01)
description = st.sidebar.text_input("Description")
date = st.sidebar.date_input("Date", value=datetime.now())


submitted = st.sidebar.button("Add Transaction")


if submitted:
    if amount <= 0:
        st.sidebar.error("❌ Amount must be greater than 0")
    elif not description.strip():
        st.sidebar.error("❌ Please enter a description")
    else:
        
        new_transaction = {
            'date': date.strftime('%Y-%m-%d'),
            'type': trans_type,
            'category': category,
            'amount': amount,
            'description': description
        }

        
        new_df = pd.DataFrame([new_transaction])
        updated_df = pd.concat([df, new_df], ignore_index=True)

        
        updated_df.to_csv('transactions.csv', index=False)

        st.sidebar.success(f"✅ {trans_type} of ${amount} saved!")
        st.rerun()


col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Summary")
    if not df.empty:
        total_income = df[df['type'] == 'Income']['amount'].sum()
        total_expenses = df[df['type'] == 'Expense']['amount'].sum()
        balance = total_income - total_expenses

        st.metric("Total Income", f"${total_income:,.2f}")
        st.metric("Total Expenses", f"${total_expenses:,.2f}")
        st.metric("Current Balance", f"${balance:,.2f}")
    else:
        st.info("No transactions yet. Add your first transaction!")

with col2:
    st.subheader("Spending by Category")
    if not df.empty:
        expense_df = df[df['type'] == 'Expense']
        if not expense_df.empty:
            category_totals = expense_df.groupby('category')['amount'].sum()
            fig, ax = plt.subplots()
            ax.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%')
            st.pyplot(fig)
        else:
            st.info("No expenses recorded yet")
    else:
        st.info("No data to display")


st.subheader("Transaction History")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No transactions yet. Add your first transaction using the sidebar!")


st.caption("💡 Tip: Track your daily spending to understand your financial habits!")
