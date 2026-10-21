(() => {
	const CART_KEY = "ga_cart";
	const SYMBOL = window.GA_CURRENCY_SYMBOL || window.GA_CURRENCY || "";
	const ITEMS = Object.fromEntries((window.GA_ITEMS || []).map((i) => [i.name, i]));

	const readCart = () => {
		try {
			return JSON.parse(localStorage.getItem(CART_KEY)) || [];
		} catch {
			return [];
		}
	};

	const writeCart = (cart) => localStorage.setItem(CART_KEY, JSON.stringify(cart));
	const money = (v) => (SYMBOL ? `${SYMBOL} ` : "") + (v || 0).toFixed(2);
	const total = (cart) => cart.reduce((s, l) => s + (ITEMS[l.item]?.price || 0) * l.qty, 0);

	const addItem = (item) => {
		const cart = readCart();
		const line = cart.find((l) => l.item === item);
		if (line) line.qty += 1;
		else cart.push({ item, qty: 1 });
		writeCart(cart);
		render();
	};

	const changeQty = (item, delta) => {
		let cart = readCart();
		const line = cart.find((l) => l.item === item);
		if (!line) return;
		line.qty += delta;
		if (line.qty <= 0) cart = cart.filter((l) => l.item !== item);
		writeCart(cart);
		render();
	};

	const render = () => {
		const el = document.getElementById("ga-cart");
		if (!el) return;

		const cart = readCart();
		if (!cart.length) {
			el.innerHTML = '<p class="ga-empty">Your cart is empty.</p>';
			return;
		}

		el.innerHTML = cart
			.map((l) => {
				const item = ITEMS[l.item] || {};
				const name = item.item_name || l.item;
				return `
					<div class="ga-line">
						<span class="ga-line__name">${name} &times; ${l.qty}</span>
						<span class="ga-product__side">
							<span class="ga-price">${money((item.price || 0) * l.qty)}</span>
							<span class="ga-qty">
								<button data-qty="-1" data-item="${l.item}" aria-label="Remove one ${name}">&minus;</button>
								<button data-qty="1" data-item="${l.item}" aria-label="Add one ${name}">+</button>
							</span>
						</span>
					</div>`;
			})
			.join("");

		el.insertAdjacentHTML(
			"beforeend",
			`<div class="ga-total">
				<span>Total</span><span>${money(total(cart))}</span>
			</div>`
		);
	};

	const checkout = async () => {
		const cart = readCart();
		if (!cart.length) {
			frappe.show_alert({ message: "Your cart is empty", indicator: "orange" });
			return;
		}
		if (frappe.session.user === "Guest") {
			window.location.href = "/login?redirect-to=/shop";
			return;
		}

		const btn = document.getElementById("ga-checkout");
		btn.disabled = true;
		btn.textContent = "Placing order…";

		try {
			const invoice = await frappe.xcall("accountsapp.api.create_order", {
				cart: JSON.stringify(cart),
			});
			writeCart([]);
			render();
			frappe.show_alert({ message: `Invoice ${invoice} created`, indicator: "green" });
		} catch (err) {
			console.error(err);
			let msg = "Could not place order";
			try {
				const data = typeof err === "string" ? JSON.parse(err) : err;
				const raw = data?._server_messages;
				if (raw) msg = JSON.parse(JSON.parse(raw)[0]).message;
			} catch {}
			frappe.show_alert({ message: msg, indicator: "red" });
		} finally {
			btn.disabled = false;
			btn.textContent = "Checkout";
		}
	};

	document.addEventListener("DOMContentLoaded", () => {
		document.querySelectorAll("[data-add-item]").forEach((btn) =>
			btn.addEventListener("click", () => addItem(btn.dataset.addItem))
		);
		document.getElementById("ga-cart")?.addEventListener("click", (e) => {
			const b = e.target.closest("[data-qty]");
			if (b) changeQty(b.dataset.item, Number(b.dataset.qty));
		});
		document.getElementById("ga-checkout")?.addEventListener("click", checkout);
		render();
	});
})();
