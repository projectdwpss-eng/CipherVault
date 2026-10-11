import random
import streamlit as st

# ============================================================
#                  ENCRYPTION FUNCTIONS (same as your project)
# ============================================================

def encrypt_message(message):
    encrypted = []
    rank = []
    ran1k = []

    for char in message:
        x = ord(char)
        current_rank = random.randint(1, 9)
        current_ran1k = random.randint(1, 9)

        rank.append(current_rank)
        ran1k.append(current_ran1k)

        # Linear transformation
        val = current_rank * x + current_ran1k
        encrypted.append(val)

    return encrypted, rank, ran1k


def decrypt_message(encrypted, rank, ran1k):
    decrypted = ""
    for i, y in enumerate(encrypted):
        x = (y - ran1k[i]) // rank[i]
        decrypted += chr(x)
    return decrypted


def parse_numbers(text):
    """Turn '12 34 56' into [12, 34, 56]. Returns None if invalid."""
    try:
        return [int(n) for n in text.split()]
    except ValueError:
        return None


# ============================================================
#                  PAGE SETUP
# ============================================================

st.set_page_config(page_title="CipherVault", page_icon="🔒")

st.title("🔒 CipherVault")
st.caption("Linear Encryption Tool")

tab_encrypt, tab_decrypt, tab_about = st.tabs(
    ["🔐 Encrypt", "🔓 Decrypt", "ℹ️ About"]
)

# ============================================================
#                  ENCRYPT TAB
# ============================================================

with tab_encrypt:
    st.subheader("Encrypt a message")

    message = st.text_area("Enter your secret message:")

    if st.button("Encrypt"):
        if not message.strip():
            st.error("Message cannot be empty.")
        else:
            encrypted, rank, ran1k = encrypt_message(message)
            # session_state remembers values between button clicks
            st.session_state["message"] = message
            st.session_state["encrypted"] = encrypted
            st.session_state["rank"] = rank
            st.session_state["ran1k"] = ran1k
            st.success("Message encrypted successfully!")

    if "encrypted" in st.session_state:
        encrypted = st.session_state["encrypted"]
        rank = st.session_state["rank"]
        ran1k = st.session_state["ran1k"]
        message = st.session_state["message"]

        st.markdown("### Ciphertext")
        st.code(" ".join(map(str, encrypted)))

        st.markdown("### Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Characters", len(message))
        col2.metric("Cipher values", len(encrypted))
        col3.metric("Ciphertext length", len(" ".join(map(str, encrypted))))

        with st.expander("🔑 View encryption keys"):
            st.write("Rank keys:")
            st.code(" ".join(map(str, rank)))
            st.write("Random keys:")
            st.code(" ".join(map(str, ran1k)))
            st.warning("Keep these keys private if you want to decrypt the message later.")

        if st.button("🔓 Decrypt this message"):
            original = decrypt_message(encrypted, rank, ran1k)
            st.success("Decryption successful!")
            st.write("Original message:")
            st.info(original)

        # Save to file (download button)
        file_text = (
            "CIPHERVAULT ENCRYPTION DATA\n"
            + "=" * 40 + "\n"
            + "Ciphertext:\n" + " ".join(map(str, encrypted)) + "\n\n"
            + "Rank Keys:\n" + " ".join(map(str, rank)) + "\n\n"
            + "Random Keys:\n" + " ".join(map(str, ran1k)) + "\n"
        )
        st.download_button(
            "💾 Download encryption data",
            data=file_text,
            file_name="ciphertext.txt",
        )

# ============================================================
#                  DECRYPT TAB
# ============================================================

with tab_decrypt:
    st.subheader("Decrypt a message")
    st.write("Paste the ciphertext and both key lists (numbers separated by spaces).")

    c_text = st.text_area("Ciphertext:")
    r_text = st.text_area("Rank keys:")
    k_text = st.text_area("Random keys:")

    if st.button("Decrypt"):
        c = parse_numbers(c_text)
        r = parse_numbers(r_text)
        k = parse_numbers(k_text)

        if not c or not r or not k:
            st.error("Please enter valid numbers in all three boxes.")
        elif not (len(c) == len(r) == len(k)):
            st.error("All three lists must have the same number of values.")
        elif 0 in r:
            st.error("Rank keys cannot be 0.")
        else:
            try:
                st.success("Decryption successful!")
                st.info(decrypt_message(c, r, k))
            except (ValueError, OverflowError):
                st.error("Could not decrypt. Check that your keys are correct.")

# ============================================================
#                  ABOUT TAB
# ============================================================

with tab_about:
    st.subheader("About CipherVault")
    st.write(
        "CipherVault is an educational encryption demonstration "
        "that uses a randomized linear transformation."
    )

    st.write("**Encryption formula:**")
    st.code("Encrypted Value = Rank × ASCII Value + Random Key")

    st.write("**Decryption formula:**")
    st.code("ASCII Value = (Encrypted Value - Random Key) / Rank")

    st.write("**Features:**")
    st.markdown(
        "- Character-level randomized keys\n"
        "- Encryption and decryption\n"
        "- Ciphertext statistics\n"
        "- File export\n"
        "- Interactive web interface"
    )

    st.warning(
        "SECURITY NOTICE: This algorithm is for educational purposes. "
        "It should not be used to protect real sensitive data."
    )