<template>
    <div class="footer">
        <div class="footer-container">
            <div class="flex flex-gap">
                <div class="bold-text">이메일주소</div>
                <div>qowlgo00@naver.com</div>
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
</style>