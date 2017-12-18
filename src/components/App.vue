<template>
  <div class="columns">
    <div class="column">
      <div class="field">
        <form id="dz"
              action="/api/simplify"
              method="post"
              enctype="multipart/form-data">
          <div class="file is-large is-boxed">
            <label class="file-label">
              <input class="file-input" type="file" name="file" />
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fa fa-upload"></i>
                </span>
                <span class="file-label">
                  Large file…
                </span>
              </span>
            </label>
          </div>
        </form>
      </div>
    </div>
    <div class="column">
      <img id="response" />
    </div>
  </div>
</template>

<style scoped></style>

<script>
</script>
