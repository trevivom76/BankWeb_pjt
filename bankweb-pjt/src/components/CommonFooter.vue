<template>
    <div class="footer">
        <div class="footer-container">
            <div class="flex flex-gap ga-4">
                <a href="https://github.com/Bang-Bang-Bank/BankWeb_pjt" class="d-flex ga-2">
                    <img src="@/assets/icon/github-icon.png" height="20px" alt="">
                    <div class="bold-text">Team Github</div>
                </a>
                |
                <div class="bold-text">Developer</div>
                <a href="https://github.com/shimkwkr" class="developer">
                    Shimkwkr
                </a>
                <a href="https://github.com/BaeJihae" class="developer">
                    Baejihae
                </a>
                <a href="https://github.com/trevivom" class="developer">
                    Taesungwon
                </a>
            </div>
            <div>
                <p class="copyright">
                    Copyright ⓒ BANG BANG BANK, All Rights Reserved.
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>

</script>

<style scoped>
.footer {
    background-color: white;
    height: 100px;
}

.footer-container {
    display: flex;
    flex-direction: column;
    padding-top: 20px;
    gap: 4px;
    justify-items: center;
    align-items: self-start;
}

.flex-gap {
    gap: 8px;
}

.bold-text {
    font-weight: 700;
    color: #424242;
}

.copyright {
    font-weight: 300;
    font-size: 14px;
}

.developer {
    font-weight: 300;
    font-size: 15px;
    text-decoration: none;
    color: #444444;
}
</style>